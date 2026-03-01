import os
import functions_framework
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

# Carrega contexto base da igreja
with open("church-context-gemini.txt", "r", encoding="utf-8") as f:
    CHURCH_CONTEXT = f.read()

@functions_framework.http
def main(request):
    # Recebe mensagem do Meta webhook ou teste
    data = request.get_json(silent=True) or {}
    user_message = data.get("message") or request.args.get("message") or ""
    if not user_message:
        return "Envie uma mensagem para obter resposta da IA da igreja ADMC."

    # Monta prompt para Gemini
    prompt = f"Contexto da igreja:\n{CHURCH_CONTEXT}\n\nPergunta do usuário: {user_message}\nResposta detalhada:" 

    # Chama Gemini API
    import os
    import time
    import re
    import json
    import requests
    import functions_framework
    from google.cloud import secretmanager
    from google.api_core import exceptions as google_exceptions

    # Configuration
    _SECRET_NAME = os.environ.get("GEMINI_SECRET_NAME", "GEMINI_API_KEY")
    _PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    _MAX_RETRIES = 3
    _RETRY_BACKOFF = 2

    # Secret Manager client and in-memory cache
    _secret_client = secretmanager.SecretManagerServiceClient()
    _GEMINI_API_KEY = None

    # Load church context file once
    with open("church-context-gemini.txt", "r", encoding="utf-8") as f:
        CHURCH_CONTEXT = f.read()


    def _get_secret(secret_name: str, project_id: str) -> str:
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        try:
            response = _secret_client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except google_exceptions.GoogleAPICallError as e:
            raise RuntimeError(f"Failed to access secret {secret_name}: {e}")


    def _ensure_api_key() -> None:
        global _GEMINI_API_KEY
        if _GEMINI_API_KEY:
            return
        if not _PROJECT_ID:
            raise RuntimeError("GOOGLE_CLOUD_PROJECT (or GCP_PROJECT) env var must be set to read secrets")
        _GEMINI_API_KEY = _get_secret(_SECRET_NAME, _PROJECT_ID)


    def _sanitize_input(text: str, max_len: int = 1000) -> str:
        if not text:
            return ""
        # Remove code fences and excessive whitespace
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = re.sub(r"[`\n]{1,}", " ", text)
        text = text.strip()
        if len(text) > max_len:
            text = text[:max_len]
        return text


    @functions_framework.http
    def main(request):
        try:
            _ensure_api_key()
        except Exception as e:
            return (f"Server misconfiguration: unable to load Gemini API key: {e}"), 500

        data = request.get_json(silent=True) or {}
        user_message = data.get("message") or request.args.get("message") or ""
        user_message = _sanitize_input(user_message, max_len=800)
        if not user_message:
            return "Envie uma mensagem para obter resposta da IA da igreja ADMC.", 400

        prompt = (
            f"Contexto da igreja:\n{CHURCH_CONTEXT}\n\nPergunta do usuário: {user_message}\nResposta detalhada:"
        )

        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={_GEMINI_API_KEY}"

        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                resp = requests.post(url, json=payload, timeout=15)
                if resp.status_code == 200:
                    body = resp.json()
                    # Defensive parsing
                    try:
                        gemini_reply = body["candidates"][0]["content"]["parts"][0]["text"]
                        return gemini_reply
                    except Exception:
                        return ("Erro: resposta inesperada do Gemini", 502)

                # Retry on server errors or rate limits
                if resp.status_code in (429, 500, 502, 503, 504):
                    if attempt < _MAX_RETRIES:
                        time.sleep(_RETRY_BACKOFF ** attempt)
                        continue
                    else:
                        return (f"Erro ao consultar Gemini (status {resp.status_code}): {resp.text}", 502)

                # For other client errors, return message
                return (f"Erro ao consultar Gemini (status {resp.status_code}): {resp.text}", 400)

            except requests.exceptions.RequestException as e:
                if attempt < _MAX_RETRIES:
                    time.sleep(_RETRY_BACKOFF ** attempt)
                    continue
                return (f"Erro de rede ao consultar Gemini: {e}", 502)
