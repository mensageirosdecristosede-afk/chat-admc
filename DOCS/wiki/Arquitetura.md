# Arquitetura — Chat ADMC

## Visão Geral

```
Usuário WhatsApp
      │
      │ 1. Envia mensagem para +55 11 91181-1106
      ▼
META PLATFORM
  WhatsApp Business Cloud API
  WABA ID: 1625049158692690
  Phone ID: 1051155144750870
      │
      │ 2. Webhook POST (JSON) + X-Hub-Signature-256
      ▼
GOOGLE CLOUD PLATFORM
  Cloud Function: chat-admc-handler (Gen1, Python 3.10, us-central1)
      │
      │ 3. Valida assinatura HMAC-SHA256
      │ 4. Busca secrets no Secret Manager
      │    • GEMINI_API_KEY
      │    • WHATSAPP_TOKEN
      │    • META_APP_SECRET
      │
      │ 5. Chama API Gemini com:
      │    • Contexto da igreja (church-context-gemini.txt)
      │    • Histórico de conversa da sessão
      │    • Mensagem do usuário
      ▼
GOOGLE AI — Gemini 2.5 Flash
      │
      │ 6. Resposta gerada pela IA (persona Sara)
      ▼
CLOUD FUNCTION
      │
      │ 7. POST para WhatsApp Cloud API (/messages)
      ▼
Usuário recebe resposta da Sara
```

---

## Componentes

### Cloud Function — `chat-admc-handler`

| Atributo | Valor |
|---|---|
| Runtime | Python 3.10 |
| Geração | Gen1 |
| Região | us-central1 |
| Projeto GCP | chat-bot-admc |
| URL | `https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler` |
| Memória | 256 MB (padrão) |
| Timeout | 60s |

**Responsabilidades:**
- Verificar assinatura do webhook Meta
- Responder verificação GET do webhook (challenge)
- Extrair mensagem do payload WhatsApp
- Gerenciar histórico de conversa por número (em memória por instância)
- Chamar Gemini AI com contexto da igreja
- Enviar resposta via WhatsApp Cloud API

### Cloud Scheduler

Dispara relatório diário às 8h (horário de Brasília) para o endpoint da Cloud Function com payload especial `{"type": "daily_report"}`.

### Secret Manager

| Secret | Conteúdo |
|---|---|
| `GEMINI_API_KEY` | Chave da API Google Gemini |
| `WHATSAPP_TOKEN` | Token do System User Meta |
| `META_APP_SECRET` | App Secret para validação de webhook |

### Cloud Storage

Armazena o arquivo de contexto da igreja (`church-context-gemini.txt`) e artefatos de deploy.

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Interface | WhatsApp Business Cloud API (Meta) |
| Compute | Google Cloud Functions Gen1 |
| IA | Google Gemini 2.5 Flash |
| Secrets | GCP Secret Manager |
| Infra como Código | Terraform |
| Linguagem | Python 3.10 |

---

## Infraestrutura como Código

Toda a infraestrutura está em `ENV-GCP/` gerenciada com Terraform:

```
ENV-GCP/
├── main.py              # Código da Cloud Function (Sara)
├── requirements.txt     # Dependências Python
├── church-context-gemini.txt  # Contexto da ADMC para o Gemini
├── cloudfunction.tf     # Cloud Function + IAM
├── scheduler.tf         # Cloud Scheduler
├── storage.tf           # Cloud Storage
├── iam.tf               # Service accounts e permissões
├── variables.tf         # Variáveis Terraform
├── terraform.tfvars     # Valores das variáveis (não commitar secrets)
└── scripts/
    ├── deploy_terraform.sh          # Deploy completo via Terraform
    └── create_secret_version.sh     # Criar/atualizar secrets
```

---

## Diagrama de Segurança

```
Internet
   │
   │ HTTPS only
   ▼
Cloud Function ──► valida X-Hub-Signature-256 (HMAC-SHA256 com META_APP_SECRET)
   │
   │ se inválido → retorna 403
   │ se válido   →
   ▼
Secret Manager ◄── service account chat-admc-fn-sa
   │               (papel: secretmanager.secretAccessor)
   │
   └── secrets never in code or env vars plain text
```
