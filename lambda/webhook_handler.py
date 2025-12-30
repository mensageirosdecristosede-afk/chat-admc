"""
Lambda Function para processar webhooks do Meta (WhatsApp, Instagram, Facebook)
e responder usando Amazon Bedrock com Claude 3
"""

import json
import os
import boto3
import logging
import hashlib
import hmac
from datetime import datetime
from typing import Dict, Any, Optional
import requests

# Configuração de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Clientes AWS
s3_client = boto3.client('s3')
ssm_client = boto3.client('ssm')

# Variáveis de ambiente
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
META_VERIFY_TOKEN = os.environ.get('META_VERIFY_TOKEN')
META_APP_SECRET = os.environ.get('META_APP_SECRET')
WHATSAPP_PHONE_ID = os.environ.get('WHATSAPP_PHONE_ID')
META_ACCESS_TOKEN = os.environ.get('META_ACCESS_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler principal da Lambda
    """
    try:
        logger.info(f"Evento recebido: {json.dumps(event)}")
        
        # Verificação do webhook (GET)
        if event.get('httpMethod') == 'GET':
            return handle_verification(event)
        
        # Processamento de mensagens (POST)
        elif event.get('httpMethod') == 'POST':
            # Verificar assinatura do Meta
            if not verify_signature(event):
                logger.error("Assinatura inválida")
                return {
                    'statusCode': 403,
                    'body': json.dumps({'error': 'Invalid signature'})
                }
            
            return handle_message(event)
        
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }
    
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }


def handle_verification(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lida com a verificação do webhook do Meta
    """
    params = event.get('queryStringParameters', {})
    
    mode = params.get('hub.mode')
    token = params.get('hub.verify_token')
    challenge = params.get('hub.challenge')
    
    logger.info(f"Verificação - Mode: {mode}, Token matches: {token == META_VERIFY_TOKEN}")
    
    if mode == 'subscribe' and token == META_VERIFY_TOKEN:
        logger.info("Webhook verificado com sucesso")
        return {
            'statusCode': 200,
            'body': challenge,
            'headers': {
                'Content-Type': 'text/plain'
            }
        }
    else:
        logger.error("Falha na verificação do webhook")
        return {
            'statusCode': 403,
            'body': json.dumps({'error': 'Forbidden'})
        }


def verify_signature(event: Dict[str, Any]) -> bool:
    """
    Verifica a assinatura do webhook do Meta
    """
    try:
        signature = event.get('headers', {}).get('x-hub-signature-256', '')
        
        if not signature:
            logger.warning("Assinatura não encontrada no header")
            return False
        
        body = event.get('body', '')
        expected_signature = 'sha256=' + hmac.new(
            META_APP_SECRET.encode(),
            body.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    except Exception as e:
        logger.error(f"Erro ao verificar assinatura: {str(e)}")
        return False


def handle_message(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processa mensagens recebidas do Meta
    """
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Salvar payload original
        save_to_s3(body, 'incoming-messages')
        
        # Processar cada entrada
        for entry in body.get('entry', []):
            for change in entry.get('changes', []):
                value = change.get('value', {})
                
                # Mensagens do WhatsApp, Instagram ou Facebook
                if 'messages' in value:
                    messages = value.get('messages', [])
                    for message in messages:
                        process_message(message, value, change.get('field'))
        
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'success'})
        }
    
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}", exc_info=True)
        return {
            'statusCode': 200,  # Retornar 200 para não reenviar
            'body': json.dumps({'status': 'error', 'message': str(e)})
        }


def process_message(message: Dict[str, Any], value: Dict[str, Any], platform: str):
    """
    Processa uma mensagem individual e envia resposta
    """
    try:
        message_id = message.get('id')
        message_from = message.get('from')
        message_type = message.get('type')
        timestamp = message.get('timestamp')
        
        logger.info(f"Processando mensagem {message_id} de {message_from} via {platform}")
        
        # Extrair texto da mensagem
        message_text = ""
        if message_type == 'text':
            message_text = message.get('text', {}).get('body', '')
        elif message_type == 'interactive':
            message_text = message.get('interactive', {}).get('button_reply', {}).get('title', '')
        
        if not message_text:
            logger.info(f"Tipo de mensagem não suportado: {message_type}")
            return
        
        # Gerar resposta com IA
        ai_response = generate_ai_response(message_text, message_from)
        
        # Salvar conversação
        save_conversation(message_from, message_text, ai_response, platform)
        
        # Enviar resposta
        send_message(message_from, ai_response, platform, value)
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem individual: {str(e)}", exc_info=True)


def generate_ai_response(user_message: str, user_id: str) -> str:
    """
    Gera resposta usando Google Gemini API (GRATUITO - 1500 req/dia)
    """
    try:
        # Carregar contexto da igreja do S3
        church_context = load_church_context()
        
        # Prompt para o modelo
        full_prompt = f"""Você é um assistente virtual da Igreja ADMC (Assembleia de Deus Ministério Caná).
Seu papel é ajudar as pessoas com informações sobre a igreja de forma educada, acolhedora e prestativa.

Contexto da Igreja:
{church_context}

Diretrizes:
- Seja sempre educado e acolhedor
- Use uma linguagem simples e amigável
- Se não souber algo, seja honesto e ofereça contato humano
- Mantenha respostas concisas (máximo 300 palavras)
- Inclua versículos bíblicos quando apropriado
- Convide as pessoas para conhecer a igreja

Pergunta do usuário: {user_message}

Resposta:"""

        # Chamar Google Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 500,
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        # Processar resposta
        result = response.json()
        ai_response = result['candidates'][0]['content']['parts'][0]['text']
        
        logger.info(f"Resposta Gemini gerada para {user_id}: {ai_response[:100]}...")
        return ai_response.strip()
    
    except Exception as e:
        logger.error(f"Erro ao gerar resposta com Gemini: {str(e)}", exc_info=True)
        # Resposta fallback
        return """Olá! Seja bem-vindo(a) à Igreja ADMC! 🙏

Desculpe, estou com dificuldades técnicas no momento, mas ficarei feliz em ajudar.

Para informações imediatas, você pode:
- Visitar nosso site
- Ligar para nossa secretaria
- Nos visitar pessoalmente

Um membro da nossa equipe entrará em contato em breve.

Deus abençoe! 🙌"""


def load_church_context() -> str:
    """
    Carrega contexto/conhecimento da igreja do S3
    """
    try:
        # Tentar carregar arquivo de contexto do S3
        response = s3_client.get_object(
            Bucket=BUCKET_NAME,
            Key='knowledge-base/church-context.txt'
        )
        context = response['Body'].read().decode('utf-8')
        return context
    
    except s3_client.exceptions.NoSuchKey:
        logger.warning("Arquivo de contexto não encontrado no S3")
        return """Igreja ADMC - Assembleia de Deus Ministério Caná
        
Informações básicas:
- Cultos: Terça, Quinta e Domingo
- Endereço: [A CONFIGURAR]
- Telefone: [A CONFIGURAR]
- Ministérios: Louvor, Infantil, Jovens, etc.

(Configure o arquivo church-context.txt no S3 para mais detalhes)"""
    
    except Exception as e:
        logger.error(f"Erro ao carregar contexto: {str(e)}")
        return "Informações da igreja em atualização."


def send_message(recipient_id: str, message: str, platform: str, value: Dict[str, Any]):
    """
    Envia mensagem de resposta via Meta API
    """
    try:
        import requests
        
        # Determinar endpoint baseado na plataforma
        if 'whatsapp' in platform.lower():
            url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"
        else:
            # Instagram e Facebook usam endpoint similar
            url = f"https://graph.facebook.com/v18.0/me/messages"
        
        headers = {
            'Authorization': f'Bearer {META_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'messaging_product': 'whatsapp' if 'whatsapp' in platform.lower() else 'instagram',
            'recipient_type': 'individual',
            'to': recipient_id,
            'type': 'text',
            'text': {
                'body': message
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Mensagem enviada com sucesso para {recipient_id}")
        
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {str(e)}", exc_info=True)


def save_conversation(user_id: str, user_message: str, bot_response: str, platform: str):
    """
    Salva conversação no S3 para análise e treinamento
    """
    try:
        timestamp = datetime.utcnow().isoformat()
        date_key = datetime.utcnow().strftime('%Y/%m/%d')
        
        conversation = {
            'timestamp': timestamp,
            'user_id': user_id,
            'platform': platform,
            'user_message': user_message,
            'bot_response': bot_response
        }
        
        key = f"conversations/{date_key}/{user_id}-{timestamp}.json"
        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(conversation, ensure_ascii=False, indent=2),
            ContentType='application/json'
        )
        
        logger.info(f"Conversação salva: {key}")
    
    except Exception as e:
        logger.error(f"Erro ao salvar conversação: {str(e)}")


def save_to_s3(data: Dict[str, Any], prefix: str):
    """
    Salva dados no S3
    """
    try:
        timestamp = datetime.utcnow().isoformat()
        key = f"{prefix}/{timestamp}.json"
        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(data, ensure_ascii=False, indent=2),
            ContentType='application/json'
        )
        
        logger.info(f"Dados salvos no S3: {key}")
    
    except Exception as e:
        logger.error(f"Erro ao salvar no S3: {str(e)}")
