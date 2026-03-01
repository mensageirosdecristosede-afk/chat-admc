# Changelog

Todas as mudanças neste repositório seguirão o padrão "Unreleased" → semantic versioning / releases.

## [Unreleased]

### Added (01/03/2026)
- **Integração WhatsApp Cloud API**: Webhook handler completo em `ENV-GCP/main.py`
- **Integração Gemini AI**: Chamadas à API Gemini com retries e contexto da igreja
- **Secret Manager**: Secrets para GEMINI_API_KEY, WHATSAPP_TOKEN, META_APP_SECRET
- **Validação de webhook**: Verificação de assinatura X-Hub-Signature-256
- **Documentação de status**: `ENV-GCP/STATUS.md` com estado atual do projeto

### Changed
- Cloud Function atualizada para v4 com suporte a WhatsApp + Gemini
- Service account `chat-admc-fn-sa` com permissões de Secret Manager

### Security
- Tokens e secrets movidos para GCP Secret Manager
- Histórico do git limpo de credenciais expostas

### Pending
- Verificação do Business Manager Meta (~2 dias úteis)
- Adição do número WhatsApp real (+55 11 98818-3880)

---

## [Initial]
- Inicial: adicionados arquivos do projeto e README inicial.

---

Notas:
- Use tags semânticas ao criar releases (`v1.0.0`, `v1.1.0`, ...).
- O arquivo deve ser atualizado antes de cada release com as mudanças relevantes.
