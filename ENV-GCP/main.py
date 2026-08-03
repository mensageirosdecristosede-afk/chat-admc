import os
import re
import time
import json
import hmac
import hashlib
import requests
import functions_framework
from datetime import datetime, timedelta
from google.cloud import secretmanager, firestore
from google.api_core import exceptions as google_exceptions

# Configuration
_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
_MAX_RETRIES = 3
_RETRY_BACKOFF = 2

# Número do administrador para receber relatórios e críticas/sugestões
ADMIN_PHONE = "5561985019958"

# Meta / WhatsApp env vars (can be direct values or secret names)
META_VERIFY_TOKEN = os.environ.get("META_VERIFY_TOKEN")
# META_APP_SECRET will be loaded from Secret Manager

# Secret Manager client and cache
_secret_client = None
_firestore_client = None
_GEMINI_API_KEY = None
_WHATSAPP_TOKEN = None
_META_APP_SECRET = None


def _get_firestore_client():
    global _firestore_client
    if _firestore_client is None:
        _firestore_client = firestore.Client(project=_PROJECT_ID)
    return _firestore_client


def _save_attendance(from_number: str, user_msg: str, bot_reply: str, is_feedback: bool = False):
    """Salva o atendimento no Firestore para relatório diário."""
    try:
        db = _get_firestore_client()
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        doc_ref = db.collection("attendances").document()
        doc_ref.set({
            "date": today,
            "timestamp": now,
            "from_number": from_number,
            "user_message": user_msg[:500],
            "bot_reply": bot_reply[:500],
            "is_feedback": is_feedback,
            "reported": False
        })
    except Exception as e:
        print(f"Erro ao salvar atendimento: {e}")


def _get_secret_client():
    global _secret_client
    if _secret_client is None:
        _secret_client = secretmanager.SecretManagerServiceClient()
    return _secret_client


def _get_secret_or_env(secret_name: str, env_var: str) -> str:
    """Try to get value from Secret Manager, fallback to env var."""
    # First check if env var has a direct value (not a secret name reference)
    env_value = os.environ.get(env_var)
    if env_value and not env_value.startswith("projects/"):
        # Check if it looks like a token (long string) vs a secret name
        if len(env_value) > 50:  # Likely a direct token value
            return env_value
    
    # Try Secret Manager
    if _PROJECT_ID:
        try:
            client = _get_secret_client()
            name = f"projects/{_PROJECT_ID}/secrets/{secret_name}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8").strip()
        except Exception as e:
            print(f"Secret Manager access error for {secret_name}: {e}")
    
    # Fallback to env var
    return env_value or ""

# Load church context
try:
    context_path = os.path.join(os.path.dirname(__file__), "church-context-gemini.txt")
    with open(context_path, "r", encoding="utf-8") as f:
        CHURCH_CONTEXT = f.read()
except FileNotFoundError:
    CHURCH_CONTEXT = ""


def _ensure_api_key() -> None:
    global _GEMINI_API_KEY
    if _GEMINI_API_KEY:
        return
    _GEMINI_API_KEY = _get_secret_or_env("GEMINI_API_KEY", "GEMINI_API_KEY")
    if not _GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not found in Secret Manager or env var")


def _ensure_whatsapp_token() -> str:
    global _WHATSAPP_TOKEN
    if _WHATSAPP_TOKEN:
        return _WHATSAPP_TOKEN
    _WHATSAPP_TOKEN = _get_secret_or_env("WHATSAPP_TOKEN", "WHATSAPP_TOKEN")
    return _WHATSAPP_TOKEN


def _ensure_app_secret() -> str:
    global _META_APP_SECRET
    if _META_APP_SECRET:
        return _META_APP_SECRET
    _META_APP_SECRET = _get_secret_or_env("META_APP_SECRET", "META_APP_SECRET")
    return _META_APP_SECRET


def _sanitize_input(text: str, max_len: int = 1000) -> str:
    if not text:
        return ""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"[`\n]{1,}", " ", text)
    text = text.strip()
    if len(text) > max_len:
        text = text[:max_len]
    return text


def _verify_signature(request) -> bool:
    """Verify X-Hub-Signature-256 header using META_APP_SECRET."""
    app_secret = _ensure_app_secret()
    if not app_secret:
        return False
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        return False
    try:
        sig_parts = signature.split("=")
        if len(sig_parts) != 2:
            return False
        algo, sig_hash = sig_parts
        if algo.lower() != "sha256":
            return False
        body = request.get_data() or b""
        mac = hmac.new(app_secret.encode("utf-8"), msg=body, digestmod=hashlib.sha256)
        expected = mac.hexdigest()
        return hmac.compare_digest(expected, sig_hash)
    except Exception:
        return False


def _call_gemini(prompt: str) -> str:
    _ensure_api_key()
    if not _GEMINI_API_KEY:
        return ("Eita, estou sem acesso ao serviço de IA no momento. "
                "Tente novamente mais tarde ou ligue pra secretaria: (61) 3205-6711")
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={_GEMINI_API_KEY}"
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            resp = requests.post(url, json=payload, timeout=15)
            if resp.status_code == 200:
                body = resp.json()
                try:
                    return body["candidates"][0]["content"]["parts"][0]["text"]
                except Exception:
                    return "Erro: resposta inesperada do Gemini"
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < _MAX_RETRIES:
                time.sleep(_RETRY_BACKOFF ** attempt)
                continue
            return f"Erro ao consultar Gemini (status {resp.status_code}): {resp.text}"
        except requests.exceptions.RequestException as e:
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_BACKOFF ** attempt)
                continue
            return f"Erro de rede ao consultar Gemini: {e}"


def _send_whatsapp_message(phone_number_id: str, to_number: str, text: str) -> bool:
    token = _ensure_whatsapp_token()
    if not token:
        print("WhatsApp token not found; cannot send message")
        return False
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"messaging_product": "whatsapp", "to": to_number, "type": "text", "text": {"body": text}}
    try:
        r = requests.post(url, headers=headers, json=body, timeout=10)
        print(f"WhatsApp send status: {r.status_code}, body: {r.text}")
        return r.status_code in (200, 201)
    except requests.RequestException:
        print("Exception when sending WhatsApp message")
        return False


def _is_feedback_message(text: str) -> bool:
    """Detecta se a mensagem contém crítica, sugestão ou reclamação."""
    keywords = [
        "sugest", "critic", "reclam", "melhora", "poderia", "deveria",
        "problema", "erro", "bug", "não funciona", "nao funciona",
        "péssimo", "pessimo", "ruim", "horrível", "horrivel",
        "feedback", "opinião", "opiniao", "avalia"
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)


def _send_feedback_alert(phone_number_id: str, from_number: str, user_msg: str, bot_reply: str):
    """Envia alerta de feedback/crítica em tempo real para o admin."""
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    report = f"""⚠️ *FEEDBACK RECEBIDO*

📅 {now}
📱 De: {from_number}

💬 *Mensagem:*
{user_msg}

🤖 *Resposta da Sara:*
{bot_reply[:500]}"""
    
    _send_whatsapp_message(phone_number_id, ADMIN_PHONE, report)


@functions_framework.http
def main(request):
    # Webhook verification (GET)
    if request.method == "GET":
        mode = request.args.get("hub.mode") or request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        verify_token = request.args.get("hub.verify_token")
        if mode == "subscribe" and verify_token and META_VERIFY_TOKEN and verify_token == META_VERIFY_TOKEN:
            return (challenge or ""), 200
        return "Forbidden", 403

    # POST: incoming webhook
    if request.method == "POST":
        # Verify signature if app secret is set
        app_secret = _ensure_app_secret()
        if app_secret and not _verify_signature(request):
            return "Invalid signature", 403

        payload = request.get_json(silent=True) or {}
        # WhatsApp Cloud API uses entry[].changes[].value.messages
        entries = payload.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages") or []
                metadata = value.get("metadata", {})
                phone_number_id = metadata.get("phone_number_id")
                for msg in messages:
                    # Only handle text messages for now
                    text_obj = msg.get("text") or {}
                    text = text_obj.get("body")
                    from_number = msg.get("from")
                    if not text or not from_number:
                        continue
                    
                    # Não processar mensagens do próprio admin (evita loop)
                    if from_number == ADMIN_PHONE:
                        continue
                    
                    user_message = _sanitize_input(text, max_len=800)
                    prompt = f"Contexto da igreja:\n{CHURCH_CONTEXT}\n\nPergunta do usuário: {user_message}\nResposta detalhada:"
                    reply = _call_gemini(prompt)
                    
                    # Send reply back via WhatsApp Cloud API
                    if phone_number_id:
                        _send_whatsapp_message(phone_number_id, from_number, reply)
                        
                        # Detectar se é feedback/crítica/sugestão
                        is_feedback = _is_feedback_message(user_message)
                        
                        # Salvar atendimento para relatório diário
                        _save_attendance(from_number, user_message, reply, is_feedback)
                        
                        # Enviar alerta imediato apenas para feedbacks/críticas
                        if is_feedback:
                            _send_feedback_alert(phone_number_id, from_number, user_message, reply)

        return "", 200

    return "Method not allowed", 405


@functions_framework.http
def send_daily_report(request):
    """Função para enviar relatório diário consolidado. Chamada pelo Cloud Scheduler."""
    try:
        db = _get_firestore_client()
        
        # Buscar atendimentos de ontem (ou hoje se for fim do dia)
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Buscar atendimentos não reportados
        docs = db.collection("attendances").where("reported", "==", False).stream()
        
        attendances = []
        feedback_count = 0
        unique_users = set()
        
        for doc in docs:
            data = doc.to_dict()
            attendances.append({
                "id": doc.id,
                "from_number": data.get("from_number", ""),
                "user_message": data.get("user_message", ""),
                "is_feedback": data.get("is_feedback", False)
            })
            unique_users.add(data.get("from_number", ""))
            if data.get("is_feedback"):
                feedback_count += 1
        
        if not attendances:
            return "Nenhum atendimento para reportar", 200
        
        # Montar relatório
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        report = f"""📊 *RELATÓRIO DIÁRIO - SARA ADMC*

📅 Gerado em: {now}
📱 Total de atendimentos: {len(attendances)}
👥 Usuários únicos: {len(unique_users)}
⚠️ Feedbacks/críticas: {feedback_count}

---
*Últimas interações:*\n"""
        
        # Adicionar até 10 últimas interações
        for att in attendances[-10:]:
            phone = att["from_number"][-4:] if len(att["from_number"]) > 4 else att["from_number"]
            msg_preview = att["user_message"][:50]
            feedback_flag = "⚠️" if att["is_feedback"] else ""
            report += f"\n• ...{phone}: {msg_preview}... {feedback_flag}"
        
        if len(attendances) > 10:
            report += f"\n\n_...e mais {len(attendances) - 10} atendimentos_"
        
        # Enviar relatório
        # Precisamos de um phone_number_id válido - usar o da última mensagem ou fixo
        token = _ensure_whatsapp_token()
        if token:
            url = "https://graph.facebook.com/v17.0/1051155144750870/messages"  # Phone number ID fixo
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            body = {"messaging_product": "whatsapp", "to": ADMIN_PHONE, "type": "text", "text": {"body": report}}
            requests.post(url, headers=headers, json=body, timeout=10)
        
        # Marcar atendimentos como reportados
        for att in attendances:
            db.collection("attendances").document(att["id"]).update({"reported": True})
        
        return f"Relatório enviado com {len(attendances)} atendimentos", 200
        
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return f"Erro: {e}", 500
