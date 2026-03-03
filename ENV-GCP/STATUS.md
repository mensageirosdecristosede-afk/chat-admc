# Status do Projeto Chat ADMC - WhatsApp + Gemini AI

**Última atualização**: 02/03/2026 22:27

## 🎉 PROJETO FUNCIONANDO!

O chatbot da ADMC está **100% operacional**!

- **Número WhatsApp**: `+55 11 91181-1106` (ADMC-Virtual)
- **Modelo IA**: Gemini 2.5 Flash
- **Status**: ✅ Em produção

---

## ✅ Concluído

### Infraestrutura GCP
- [x] Cloud Function `chat-admc-handler` deployada (v11)
  - URL: `https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler`
  - Runtime: Python 3.10
  - Region: us-central1
- [x] Service Account: `chat-admc-fn-sa@chat-bot-admc.iam.gserviceaccount.com`
  - Roles: logging.logWriter, storage.objectViewer, secretmanager.secretAccessor
- [x] API Generative Language habilitada

### Secrets no Secret Manager
- [x] `GEMINI_API_KEY` - Chave da API Gemini (v3 - criada no projeto GCP)
- [x] `WHATSAPP_TOKEN` - Token do System User do WhatsApp (v3)
- [x] `META_APP_SECRET` - App Secret para validação de webhook (v3)

### Meta/WhatsApp Configuration (Portfólio - ADMC Sede)
- [x] App "Chat ADMC" criado (App ID: `1791477378904720`) - **PUBLICADO**
- [x] System User `deploy-whatsapp` criado (ID: `61583639447019`)
- [x] Business Portfolio: "ADMC Sede" (ID: `1034751007960249`)
- [x] Verificação da empresa: ✅ Aprovada
- [x] WABA de Produção criada (ID: `1625049158692690`)
- [x] **Número de Produção**: `+55 11 91181-1106` (Phone ID: `1051155144750870`) - **CONECTADO**
- [x] Webhook configurado e verificado
  - Callback URL: `https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler`
  - Verify Token: `admc-verify-2026`
  - Assinaturas: `messages`, `message_template_status_update`

### Git/GitHub
- [x] Repositório: `mensageirosdecristosede-afk/chat-admc`
- [x] Branch: `feature/adeilson`
- [x] Secrets removidos do histórico do git

---

## 📱 Como Usar

Qualquer pessoa pode enviar uma mensagem para **+55 11 91181-1106** no WhatsApp e receberá respostas automáticas sobre a igreja ADMC!

---

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
