# Status de Produção

**Última atualização**: 2026-08-03 (v1.0.0)

---

## Componentes em Produção

| Componente | Status | Detalhes |
|---|---|---|
| Cloud Function `chat-admc-handler` | ✅ Ativo | v11, Python 3.10, us-central1 |
| WhatsApp Business API | ✅ Conectado | +55 11 91181-1106 |
| Gemini AI | ✅ Integrado | Gemini 2.5 Flash |
| Secret Manager | ✅ Configurado | 3 secrets ativos |
| Cloud Scheduler | ✅ Agendado | Relatório diário 8h BRT |
| Webhook Meta | ✅ Verificado | `messages` + `message_template_status_update` |

---

## Endpoints

| Endpoint | URL |
|---|---|
| Cloud Function | `https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler` |

---

## Projeto GCP

| Atributo | Valor |
|---|---|
| Project ID | `chat-bot-admc` |
| Region | `us-central1` |
| Service Account | `chat-admc-fn-sa@chat-bot-admc.iam.gserviceaccount.com` |

---

## Histórico de Versões

| Versão | Data | Principais mudanças |
|---|---|---|
| v1.0.0 | 2026-08-03 | Sara IA: persona, versículos, relatório diário, resiliência operacional |
| Initial | 2026-01-03 | Estrutura inicial do projeto |

---

## Custos

Operação dentro dos limites do **free tier GCP**:
- Cloud Functions: free tier generoso para volume de mensagens da igreja
- Gemini API: cota gratuita suficiente para uso pastoral
- Secret Manager: gratuito para poucos secrets
- Cloud Scheduler: 3 jobs gratuitos/mês

Para detalhes de custo projetado: [DOCS/CUSTOS.md](../CUSTOS.md)

---

## Como Verificar Saúde do Sistema

```bash
# 1. Verificar logs recentes
gcloud functions logs read chat-admc-handler \
  --region us-central1 \
  --project chat-bot-admc \
  --limit 20

# 2. Testar webhook verification
curl "https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler?hub.mode=subscribe&hub.verify_token=admc-verify-2026&hub.challenge=ping"
# Esperado: ping

# 3. Verificar secrets
gcloud secrets versions list GEMINI_API_KEY --project chat-bot-admc
gcloud secrets versions list WHATSAPP_TOKEN --project chat-bot-admc
```
