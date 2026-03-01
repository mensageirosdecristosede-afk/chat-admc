# Custo e Otimização AWS Free Tier

## 💰 Análise de Custos

### Serviços Utilizados

| Serviço | Free Tier | Estimativa Mensal | Status |
|---------|-----------|-------------------|--------|
| **Lambda** | 1M requisições<br/>400.000 GB-s compute | ~10.000 msgs/mês | ✅ Grátis |
| **API Gateway** | 1M requisições | ~10.000 msgs/mês | ✅ Grátis |
| **S3** | 5GB storage<br/>20.000 GET<br/>2.000 PUT | < 1GB<br/>~5.000 reads<br/>~5.000 writes | ✅ Grátis |
| **CloudWatch Logs** | 5GB ingest<br/>5GB storage | < 500MB/mês | ✅ Grátis |
| **Bedrock Claude 3** | Sem free tier | Depende do uso | ⚠️ Pago |

### Bedrock Pricing (us-east-1)

**Claude 3 Haiku** (Recomendado - Mais econômico):
- Input: $0.00025 por 1K tokens (~750 palavras)
- Output: $0.00125 por 1K tokens (~750 palavras)

**Exemplo de cálculo**:
- Mensagem usuário: ~50 tokens ($0.0000125)
- Contexto igreja: ~1000 tokens ($0.00025)
- Resposta bot: ~200 tokens ($0.00025)
- **Total por interação: ~$0.0003125**

**Estimativa mensal**:
- 100 mensagens/mês: ~$0.03
- 500 mensagens/mês: ~$0.16
- 1000 mensagens/mês: ~$0.31
- 5000 mensagens/mês: ~$1.56

### Alternativas Gratuitas para IA

Se o Bedrock ultrapassar o orçamento, considere:

#### 1. **Hugging Face (API Gratuita)**
- Modelos como Mistral, Llama 2
- Rate limits: ~1000 req/dia
- Código de exemplo fornecido abaixo

#### 2. **OpenRouter (Free Tier)**
- Acesso a vários modelos
- Free tier com limitações
- Requer menos mudanças no código

#### 3. **Google Gemini API**
- Free tier generoso
- 60 requisições/minuto
- Fácil integração

## 📊 Monitoramento de Custos

### 1. Configurar AWS Budgets

```bash
# Criar budget de $5/mês
aws budgets create-budget \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --budget file://budget.json
```

**budget.json**:
```json
{
  "BudgetName": "ChatADMC-Monthly",
  "BudgetLimit": {
    "Amount": "5",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST"
}
```

### 2. CloudWatch Dashboard

Acesse: AWS Console > CloudWatch > Dashboards

Métricas importantes:
- Lambda invocations
- API Gateway requests
- Bedrock token usage
- S3 storage utilization

### 3. Cost Explorer

```bash
# Ver custos dos últimos 30 dias
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE
```

## 🔧 Otimizações

### 1. Reduzir Custos do Bedrock

#### a) Usar Modelo Mais Econômico

```python
# Em webhook_handler.py, linha ~180
modelId='anthropic.claude-3-haiku-20240307-v1:0'  # Mais barato
# vs
modelId='anthropic.claude-3-sonnet-20240229-v1:0'  # 5x mais caro
```

#### b) Reduzir Tamanho do Contexto

```python
# Limite o contexto carregado
def load_church_context() -> str:
    # Carregar apenas informações essenciais
    # Reduzir de 2000 para 500 tokens
    context = """[Contexto resumido]"""
    return context
```

#### c) Cache de Respostas Comuns

```python
# Adicionar cache para perguntas frequentes
COMMON_RESPONSES = {
    "horario": "Nossos cultos são...",
    "endereco": "Estamos localizados...",
    "contato": "Entre em contato pelo..."
}

def get_response(message):
    # Verificar cache primeiro
    for key, response in COMMON_RESPONSES.items():
        if key in message.lower():
            return response
    
    # Só usar Bedrock se necessário
    return generate_ai_response(message)
```

#### d) Limitar Max Tokens

```python
payload = {
    "max_tokens": 300,  # Reduzir de 500 para 300
    # ...
}
```

### 2. Otimizar Lambda

#### a) Aumentar Memória (Paradoxalmente mais barato)

```hcl
# terraform/lambda.tf
resource "aws_lambda_function" "webhook_handler" {
  memory_size = 1024  # Aumentar de 512 para 1024
  # Execução mais rápida = menos custo
}
```

#### b) Provisioned Concurrency (Evitar)

Não use provisioned concurrency - fora do free tier.

#### c) Reduzir Tamanho do Pacote

```bash
# Usar apenas bibliotecas necessárias
# Remover dependências não utilizadas
```

### 3. Otimizar S3

#### a) Lifecycle Policies

```hcl
# Já configurado em s3.tf
# - Deletar conversas antigas após 90 dias
# - Deletar logs após 30 dias
```

#### b) Inteligent-Tiering

```hcl
resource "aws_s3_bucket_intelligent_tiering_configuration" "chat_bucket" {
  bucket = aws_s3_bucket.chat_bucket.id
  name   = "EntireBucket"

  tiering {
    access_tier = "ARCHIVE_ACCESS"
    days        = 90
  }
}
```

### 4. Otimizar CloudWatch

```hcl
# Reduzir retenção de logs
resource "aws_cloudwatch_log_group" "lambda_logs" {
  retention_in_days = 3  # Reduzir de 7 para 3 dias
}
```

## 🆓 Migração para Alternativa Gratuita

### Opção: Hugging Face API

#### 1. Cadastro

```bash
# 1. Criar conta em https://huggingface.co/
# 2. Gerar token: Settings > Access Tokens
# 3. Adicionar ao SSM Parameter Store
```

#### 2. Modificar Lambda

```python
# webhook_handler.py

import requests

HF_API_TOKEN = os.environ.get('HF_API_TOKEN')
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

def generate_ai_response_hf(user_message: str, user_id: str) -> str:
    """
    Gera resposta usando Hugging Face API (GRATUITO)
    """
    try:
        church_context = load_church_context()
        
        prompt = f"""<s>[INST] Você é um assistente da Igreja ADMC.

Contexto: {church_context}

Pergunta: {user_message}

Responda de forma educada e objetiva. [/INST]"""

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 300,
                "temperature": 0.7,
                "top_p": 0.95,
                "return_full_text": False
            }
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result[0]['generated_text']
        else:
            logger.error(f"HF API error: {response.text}")
            return get_fallback_response()
    
    except Exception as e:
        logger.error(f"Erro HF: {str(e)}")
        return get_fallback_response()
```

#### 3. Atualizar Terraform

```hcl
# terraform/lambda.tf

environment {
  variables = {
    USE_HUGGINGFACE = "true"
    HF_API_TOKEN    = var.huggingface_token
    # ... outras variáveis
  }
}

# terraform/iam.tf

# Remover permissões Bedrock
# Adicionar se usar outro serviço
```

## 📈 Escalabilidade

### Limites Free Tier

| Recurso | Limite | Ação ao Atingir |
|---------|--------|-----------------|
| Lambda Invocations | 1M/mês | ~33K/dia - improvável |
| API Gateway Requests | 1M/mês | ~33K/dia - improvável |
| S3 Storage | 5GB | Implementar limpeza |
| Bedrock Tokens | Pago desde o início | Monitorar de perto |

### Alertas Recomendados

```bash
# CloudWatch Alarm para Lambda
aws cloudwatch put-metric-alarm \
  --alarm-name chat-admc-high-invocations \
  --alarm-description "Lambda invocations > 800K/mês" \
  --metric-name Invocations \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 2592000 \
  --threshold 800000 \
  --comparison-operator GreaterThanThreshold
```

## 🎯 Recomendações Finais

### Para POC (Proof of Concept)

1. ✅ Use Claude 3 Haiku (Bedrock)
2. ✅ Implemente cache de respostas
3. ✅ Configure alertas de custo
4. ✅ Monitore uso diariamente

**Custo estimado POC**: $0.50 - $2.00/mês

### Para Produção

1. Avalie custo real após POC
2. Se > $5/mês, considere Hugging Face
3. Implemente todas as otimizações
4. Configure budget de $10/mês

### Economia Máxima (100% Grátis)

1. Use Hugging Face API
2. Implemente rate limiting
3. Cache agressivo de respostas
4. Reduza retenção de logs para 1 dia

**Custo**: $0.00/mês

## 📞 Suporte

Para otimizações específicas ou dúvidas sobre custos, consulte:
- [AWS Free Tier](https://aws.amazon.com/free/)
- [Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Hugging Face](https://huggingface.co/pricing)
