# Changelog

Todas as mudanças neste repositório seguirão o padrão "Unreleased" → semantic versioning / releases.

## [Unreleased]

### Changed (02/06/2026)
- **Robustez do contexto da igreja**: leitura de `church-context-gemini.txt` agora usa caminho absoluto baseado no arquivo, evitando falhas por diretório de execução.
- **Fallback amigável para indisponibilidade de IA**: quando `GEMINI_API_KEY` não está disponível, a Sara responde mensagem de indisponibilidade em vez de encerrar o fluxo com exceção.
- **Observabilidade de secrets e envio WhatsApp**: logs explícitos para falha de acesso ao Secret Manager, ausência de token e status de envio na API da Meta.
- **Resiliência operacional**: redução de falhas silenciosas em produção quando houver problema temporário de infraestrutura/segredos.

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
