# Status do Projeto Chat ADMC - WhatsApp + Gemini AI

**Última atualização**: 01/03/2026

## ✅ Concluído

### Infraestrutura GCP
- [x] Cloud Function `chat-admc-handler` deployada
  - URL: `https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler`
  - Runtime: Python 3.10
  - Region: us-central1
- [x] Service Account: `chat-admc-fn-sa@chat-bot-admc.iam.gserviceaccount.com`
  - Roles: logging.logWriter, storage.objectViewer, secretmanager.secretAccessor

### Secrets no Secret Manager
- [x] `GEMINI_API_KEY` - Chave da API Gemini
- [x] `WHATSAPP_TOKEN` - Token do System User do WhatsApp
- [x] `META_APP_SECRET` - App Secret para validação de webhook

### Meta/WhatsApp Configuration
- [x] App "Chat ADMC" criado (App ID: `1220182596657877`)
- [x] System User `deploy-whatsapp` criado (ID: `122103726926815355`)
- [x] Business Manager "ADMC" (ID: `1562859828288738`)
- [x] Webhook configurado e verificado
  - Callback URL: `https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler`
  - Verify Token: `admc-verify-2026`
- [x] WABAs atribuídas ao System User

### Git/GitHub
- [x] Repositório: `mensageirosdecristosede-afk/chat-admc`
- [x] Branch: `feature/adeilson`
- [x] Secrets removidos do histórico do git

---

## ⏳ Em Andamento (Aguardando Meta)

### Verificação do Business Manager
- **Status**: `pending_submission` → Documentos enviados
- **Documentos**: Cartão CNPJ + verificação de e-mail @mensageirosdecristo.com
- **Previsão**: ~2 dias úteis para análise

### Número WhatsApp Real
- **Número novo**: `+55 11 98818-3880`
- **Status**: Aguardando SMS de verificação + aprovação do Business Manager

---

## 📊 Status das WABAs

| WABA | ID | Status | Números |
|------|-----|--------|---------|
| Test WhatsApp Business Account | `1515243402874226` | ✅ APPROVED | Número de teste: 15551791361 |
| ADMC Sede | `1562677358407435` | ⏳ PENDING | Nenhum (aguardando verificação) |

---

## 🔜 Próximos Passos (após aprovação da Meta)

1. **Adicionar número real** (`+55 11 98818-3880`) à WABA "ADMC Sede"
2. **Verificar número** via SMS
3. **Testar fluxo completo**: Usuário envia mensagem → Webhook → Gemini → Resposta
4. **Configurar templates** de mensagem (obrigatório para iniciar conversas)

---

## 🧪 Como Testar (com WABA de Teste)

Enquanto aguarda aprovação, pode testar com o número de teste:

1. Adicione um número pessoal como destinatário permitido no Meta Developer Console
2. Envie mensagem template:
```bash
curl -X POST "https://graph.facebook.com/v17.0/961149830411081/messages" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "SEU_NUMERO",
    "type": "template",
    "template": {"name": "hello_world", "language": {"code": "en_US"}}
  }'
```

---

## 📁 Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `ENV-GCP/main.py` | Cloud Function - Webhook handler |
| `ENV-GCP/church-context-gemini.txt` | Contexto da igreja para o Gemini |
| `ENV-GCP/requirements.txt` | Dependências Python |
| `docs/META_SETUP.md` | Configuração da integração Meta |

---

## 🔐 Variáveis de Ambiente da Cloud Function

| Variável | Valor/Secret |
|----------|--------------|
| `META_VERIFY_TOKEN` | `admc-verify-2026` |
| `GEMINI_API_KEY` | Secret Manager |
| `WHATSAPP_TOKEN` | Secret Manager |
| `META_APP_SECRET` | Secret Manager |

---

## 📞 Suporte

- **Problemas com Meta/WhatsApp**: https://business.facebook.com/business/help
- **Verificação do negócio**: https://business.facebook.com/settings/security
