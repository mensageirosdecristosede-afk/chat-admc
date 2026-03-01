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
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(GEMINI_API_URL, json=payload)
    if response.status_code == 200:
        gemini_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return gemini_reply
    else:
        return f"Erro ao consultar Gemini: {response.text}"
