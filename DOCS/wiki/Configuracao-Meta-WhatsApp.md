# Configuração Meta / WhatsApp

## App Meta

| Campo | Valor |
|---|---|
| App Name | Chat ADMC |
| App ID | `1791477378904720` |
| Status | Publicado |

---

## WhatsApp Business

| Campo | Valor |
|---|---|
| Business Portfolio | ADMC Sede (ID: `1034751007960249`) |
| WABA ID | `1625049158692690` |
| Phone ID | `1051155144750870` |
| Número | +55 11 91181-1106 |
| System User | `deploy-whatsapp` (ID: `61583639447019`) |

---

## Webhook

| Campo | Valor |
|---|---|
| Callback URL | `https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler` |
| Verify Token | `admc-verify-2026` |
| Assinaturas | `messages`, `message_template_status_update` |

### Como verificar o webhook manualmente

```bash
curl "https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler?hub.mode=subscribe&hub.verify_token=admc-verify-2026&hub.challenge=qualquer-valor"
# Deve retornar: qualquer-valor
```

---

## Tokens e Secrets

Todos os tokens estão no **GCP Secret Manager** do projeto `chat-bot-admc`:

| Secret GCP | Origem |
|---|---|
| `WHATSAPP_TOKEN` | System User token — Meta Business Suite → Configurações → Usuários do sistema |
| `META_APP_SECRET` | Meta Developer Console → App → Configurações → App Secret |
| `GEMINI_API_KEY` | Google AI Studio (aistudio.google.com) |

### Rotacionar um token

1. Gere novo token/chave no portal de origem
2. Atualize o secret no GCP:
   ```bash
   echo -n "NOVO_TOKEN" | gcloud secrets versions add NOME_DO_SECRET \
     --data-file=- \
     --project chat-bot-admc
   ```
3. A próxima invocação da Cloud Function usará automaticamente a versão mais recente

---

## Verificação de Assinatura

Cada webhook recebido da Meta tem o header `X-Hub-Signature-256`. A Cloud Function valida:

```
HMAC-SHA256(payload_raw, META_APP_SECRET) == valor_do_header
```

Requisições com assinatura inválida retornam `HTTP 403` imediatamente.

---

## Troubleshooting

| Sintoma | Provável causa | Solução |
|---|---|---|
| Sara não responde | Token expirado | Rotacionar `WHATSAPP_TOKEN` |
| 403 no webhook | App Secret desatualizado | Rotacionar `META_APP_SECRET` |
| Erro "Gemini unavailable" | API key inválida ou cota | Verificar `GEMINI_API_KEY` |
| Webhook não verificado | Verify token errado no Meta | Confirmar `admc-verify-2026` |
