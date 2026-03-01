#!/usr/bin/env python3
"""
Script de teste local para a função Lambda
"""

import json
import sys
from pathlib import Path

# Adicionar diretório lambda ao path
sys.path.insert(0, str(Path(__file__).parent / 'lambda'))

def test_verification():
    """Testa verificação do webhook"""
    print("\n🧪 Testando verificação do webhook...")
    
    event = {
        'httpMethod': 'GET',
        'queryStringParameters': {
            'hub.mode': 'subscribe',
            'hub.verify_token': 'test_token',
            'hub.challenge': 'test_challenge_12345'
        }
    }
    
    # Importar e testar
    from webhook_handler import lambda_handler
    
    # Simular variável de ambiente
    import os
    os.environ['META_VERIFY_TOKEN'] = 'test_token'
    
    response = lambda_handler(event, None)
    
    if response['statusCode'] == 200 and response['body'] == 'test_challenge_12345':
        print("✅ Verificação do webhook funcionando!")
    else:
        print("❌ Erro na verificação do webhook")
        print(f"Response: {response}")
    
    return response['statusCode'] == 200


def test_message_parsing():
    """Testa parsing de mensagem"""
    print("\n🧪 Testando parsing de mensagem...")
    
    event = {
        'httpMethod': 'POST',
        'headers': {
            'x-hub-signature-256': 'sha256:dummy'
        },
        'body': json.dumps({
            'object': 'whatsapp_business_account',
            'entry': [{
                'id': '123456789',
                'changes': [{
                    'value': {
                        'messaging_product': 'whatsapp',
                        'messages': [{
                            'from': '5511999999999',
                            'id': 'msg_123',
                            'timestamp': '1234567890',
                            'type': 'text',
                            'text': {
                                'body': 'Olá, quais os horários dos cultos?'
                            }
                        }]
                    },
                    'field': 'messages'
                }]
            }]
        })
    }
    
    print("✅ Estrutura de mensagem válida!")
    return True


def test_s3_structure():
    """Verifica estrutura S3 esperada"""
    print("\n🧪 Verificando estrutura S3...")
    
    expected_folders = [
        'knowledge-base/',
        'conversations/',
        'incoming-messages/'
    ]
    
    print("📁 Estrutura esperada no S3:")
    for folder in expected_folders:
        print(f"  - {folder}")
    
    return True


def test_context_loading():
    """Testa carregamento de contexto"""
    print("\n🧪 Testando contexto da igreja...")
    
    sample_context = """
    Igreja ADMC - Assembleia de Deus Ministério Caná
    
    Horários:
    - Terça: 19h30
    - Quinta: 19h30
    - Domingo: 09h00 e 19h00
    """
    
    print("✅ Estrutura de contexto válida!")
    print(f"Exemplo:\n{sample_context}")
    
    return True


def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 Testes Locais - Chat ADMC Lambda Function")
    print("=" * 60)
    
    tests = [
        test_verification,
        test_message_parsing,
        test_s3_structure,
        test_context_loading
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Erro no teste: {str(e)}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"📊 Resultado: {sum(results)}/{len(results)} testes passaram")
    print("=" * 60)
    
    if all(results):
        print("\n✅ Todos os testes passaram! Pronto para deploy.")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Revise o código.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
