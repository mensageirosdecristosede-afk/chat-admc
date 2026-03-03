# Arquitetura do Chat ADMC

## 📋 Visão Geral

O Chat ADMC é um chatbot inteligente que utiliza IA (Gemini) para responder automaticamente mensagens recebidas no WhatsApp da igreja Assembleia de Deus Ministério dos Mensageiros de Cristo.

**Status**: ✅ Em Produção  
**Número WhatsApp**: +55 11 91181-1106  
**Custo**: 💚 Gratuito (dentro dos limites do free tier)

---

## 🏗️ Arquitetura

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              FLUXO DE MENSAGENS                               │
└──────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │   Usuário   │
    │  WhatsApp   │
    └──────┬──────┘
           │
           │ 1️⃣ Envia mensagem
           │    "+55 11 91181-1106"
           ▼
    ┌─────────────────────────────────────────┐
    │         META PLATFORM                    │
    │  ┌─────────────────────────────────┐    │
    │  │   WhatsApp Business Cloud API   │    │
    │  │   WABA ID: 1625049158692690     │    │
    │  │   Phone ID: 1051155144750870    │    │
    │  └──────────────┬──────────────────┘    │
    │                 │                        │
    │                 │ 2️⃣ Webhook POST       │
    │                 │    (JSON payload)      │
    └─────────────────┼────────────────────────┘
                      │
                      │ HTTPS + Signature (X-Hub-Signature-256)
                      ▼
    ┌─────────────────────────────────────────┐
    │         GOOGLE CLOUD PLATFORM           │
    │  ┌─────────────────────────────────┐    │
    │  │     Cloud Function (Gen 1)      │    │
    │  │     chat-admc-handler           │    │
    │  │     Runtime: Python 3.10        │    │
    │  │     Region: us-central1         │    │
    │  └──────────────┬──────────────────┘    │
    │                 │                        │
    │    3️⃣ Valida   │  4️⃣ Busca Secrets    │
    │    assinatura   │                        │
    │                 ▼                        │
    │  ┌─────────────────────────────────┐    │
    │  │       Secret Manager            │    │
    │  │  • GEMINI_API_KEY               │    │
    │  │  • WHATSAPP_TOKEN               │    │
    │  │  • META_APP_SECRET              │    │
    │  └─────────────────────────────────┘    │
    └─────────────────┬────────────────────────┘
                      │
                      │ 5️⃣ Chama API Gemini
                      ▼
    ┌─────────────────────────────────────────┐
    │           GOOGLE AI                      │
    │  ┌─────────────────────────────────┐    │
    │  │      Gemini 2.5 Flash           │    │
    │  │      (generativelanguage API)   │    │
    │  └──────────────┬──────────────────┘    │
    │                 │                        │
    │    Prompt:      │  6️⃣ Resposta IA      │
    │    • Contexto   │                        │
    │      da igreja  │                        │
    │    • Pergunta   │                        │
    │      do usuário │                        │
    └─────────────────┼────────────────────────┘
                      │
                      │ 7️⃣ POST WhatsApp API
                      ▼
    ┌─────────────────────────────────────────┐
    │         META PLATFORM                    │
    │  ┌─────────────────────────────────┐    │
    │  │   WhatsApp Business Cloud API   │    │
    │  │   POST /messages                │    │
    │  └──────────────┬──────────────────┘    │
    └─────────────────┼────────────────────────┘
                      │
                      │ 8️⃣ Entrega mensagem
                      ▼
    ┌─────────────┐
    │   Usuário   │
    │  recebe     │
    │  resposta   │
    └─────────────┘
```

---

## 📦 Componentes

### 1. WhatsApp Business Cloud API (Meta)
- **App ID**: `1791477378904720`
- **Business Portfolio**: ADMC Sede (`1034751007960249`)
- **WABA ID**: `1625049158692690`
- **Phone Number ID**: `1051155144750870`
- **Número**: +55 11 91181-1106
- **Display Name**: ADMC-Virtual

### 2. Cloud Function (GCP)
- **Nome**: `chat-admc-handler`
- **URL**: `https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler`
- **Runtime**: Python 3.10
- **Memória**: 256 MB
- **Timeout**: 60s
- **Service Account**: `chat-admc-fn-sa@chat-bot-admc.iam.gserviceaccount.com`

### 3. Secret Manager (GCP)
| Secret | Descrição |
|--------|-----------|
| `GEMINI_API_KEY` | Chave da API Gemini |
| `WHATSAPP_TOKEN` | Token do System User Meta |
| `META_APP_SECRET` | App Secret para validação de webhook |

### 4. Gemini AI (Google)
- **Modelo**: `gemini-2.5-flash`
- **API**: `generativelanguage.googleapis.com`
- **Contexto**: Arquivo `church-context-gemini.txt`

---

## 💰 Custos (Free Tier)

| Serviço | Limite Gratuito | Uso Esperado |
|---------|-----------------|--------------|
| **Cloud Functions** | 2M invocações/mês | ~10K/mês |
| **Gemini API** | 1500 req/dia | ~500/dia |
| **WhatsApp API** | Conversas iniciadas pelo cliente grátis 24h | ✅ |
| **Secret Manager** | 10K acessos/mês | ~1K/mês |

**Custo total estimado: R$ 0,00** (dentro do free tier)

---

## 🔐 Segurança

1. **Validação de Webhook**: Toda requisição é validada com `X-Hub-Signature-256` usando o `META_APP_SECRET`
2. **Secrets**: Credenciais armazenadas no Secret Manager (não em código)
3. **Service Account**: Permissões mínimas necessárias (princípio do menor privilégio)
4. **HTTPS**: Todas as comunicações são criptografadas

---

## 📁 Arquivos Principais

```
ENV-GCP/
├── main.py                    # Cloud Function (webhook handler)
├── requirements.txt           # Dependências Python
├── church-context-gemini.txt  # Contexto da igreja para o Gemini
├── STATUS.md                  # Status do projeto
├── cloudfunction.tf           # Terraform (infra as code)
├── provider.tf                # Configuração GCP
└── variables.tf               # Variáveis do Terraform
```

---

## 🔄 Fluxo Detalhado

### 1. Recebimento da Mensagem
```python
# Webhook recebe POST do Meta
payload = request.get_json()
# Extrai mensagem do payload
messages = payload["entry"][0]["changes"][0]["value"]["messages"]
```

### 2. Validação de Assinatura
```python
# Valida X-Hub-Signature-256
signature = request.headers.get("X-Hub-Signature-256")
mac = hmac.new(app_secret, body, hashlib.sha256)
expected = mac.hexdigest()
hmac.compare_digest(expected, signature)
```

### 3. Chamada ao Gemini
```python
# Monta prompt com contexto
prompt = f"Contexto da igreja:\n{CHURCH_CONTEXT}\n\nPergunta: {user_message}"

# Chama API Gemini
response = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
    json={"contents": [{"parts": [{"text": prompt}]}]}
)
```

### 4. Resposta ao Usuário
```python
# Envia resposta via WhatsApp API
requests.post(
    f"https://graph.facebook.com/v17.0/{phone_number_id}/messages",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "messaging_product": "whatsapp",
        "to": from_number,
        "text": {"body": reply}
    }
)
```

---

## 🚀 Deploy

```bash
# Deploy da Cloud Function
cd ENV-GCP
gcloud functions deploy chat-admc-handler \
  --runtime=python310 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point=main \
  --region=us-central1 \
  --project=chat-bot-admc \
  --service-account=chat-admc-fn-sa@chat-bot-admc.iam.gserviceaccount.com \
  --set-env-vars=META_VERIFY_TOKEN=admc-verify-2026,GOOGLE_CLOUD_PROJECT=chat-bot-admc
```

---

## 📊 Monitoramento

### Logs
```bash
gcloud functions logs read chat-admc-handler \
  --project=chat-bot-admc \
  --region=us-central1 \
  --limit=50
```

### Métricas
- [Cloud Functions Console](https://console.cloud.google.com/functions?project=chat-bot-admc)
- [Meta Business Suite](https://business.facebook.com/)

---

## 🆘 Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| 403 Invalid signature | App Secret incorreto | Atualizar `META_APP_SECRET` |
| 404 Model not found | Modelo Gemini desatualizado | Usar `gemini-2.5-flash` |
| 429 Quota exceeded | Limite de requisições | Aguardar ou upgrade |
| Mensagem não chega | Webhook não assinado | Ativar assinatura `messages` |

---

*Última atualização: 02/03/2026*
