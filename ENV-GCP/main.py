import os
import re
import time
import json
import hmac
import hashlib
import requests
import functions_framework
from google.cloud import secretmanager
from google.api_core import exceptions as google_exceptions

# Configuration
_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
_MAX_RETRIES = 3
_RETRY_BACKOFF = 2

# Meta / WhatsApp env vars (can be direct values or secret names)
META_VERIFY_TOKEN = os.environ.get("META_VERIFY_TOKEN")
# META_APP_SECRET will be loaded from Secret Manager

# Secret Manager client and cache
_secret_client = None
_GEMINI_API_KEY = None
_WHATSAPP_TOKEN = None
_META_APP_SECRET = None


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
        except Exception:
            pass
    
    # Fallback to env var
    return env_value or ""

# Load church context
try:
    with open("church-context-gemini.txt", "r", encoding="utf-8") as f:
        CHURCH_CONTEXT = f.read()
except FileNotFoundError:
    CHURCH_CONTEXT = ""


def _ensure_api_key() -> None:
    global _GEMINI_API_KEY
    if _GEMINI_API_KEY:
        return
    _GEMINI_API_KEY = _get_secret_or_env("GEMINI_API_KEY", "GEMINI_API_KEY")
    if not _GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not found in Secret Manager or env var")


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
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={_GEMINI_API_KEY}"
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
        return False
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"messaging_product": "whatsapp", "to": to_number, "type": "text", "text": {"body": text}}
    try:
        r = requests.post(url, headers=headers, json=body, timeout=10)
        return r.status_code in (200, 201)
    except requests.RequestException:
        return False


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
                    user_message = _sanitize_input(text, max_len=800)
                    prompt = f"Contexto da igreja:\n{CHURCH_CONTEXT}\n\nPergunta do usuário: {user_message}\nResposta detalhada:"
                    reply = _call_gemini(prompt)
                    # Send reply back via WhatsApp Cloud API
                    if phone_number_id:
                        _send_whatsapp_message(phone_number_id, from_number, reply)

        return "", 200

    return "Method not allowed", 405
