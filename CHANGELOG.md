# Changelog

Todas as mudanças neste repositório seguirão o padrão "Unreleased" → semantic versioning / releases.

## [Unreleased]

---

## [1.0.0] - 2026-08-03

### Added
- **Persona Sara**: bot humanizado com nome, estilo pastoral e linguagem acolhedora
- **Versículos diários e conteúdo de relacionamento**: Sara envia versículos temáticos e dicas de relacionamento saudável baseadas em valores cristãos
- **Relatório diário consolidado**: função de envio automático via Cloud Scheduler com resumo das interações
- **Integração WhatsApp Cloud API**: Webhook handler completo em `ENV-GCP/main.py`
- **Integração Gemini AI**: Chamadas à API Gemini com retries, contexto da igreja e histórico de conversa por sessão
- **Secret Manager**: Secrets para `GEMINI_API_KEY`, `WHATSAPP_TOKEN`, `META_APP_SECRET` gerenciados no GCP
- **Validação de webhook**: Verificação de assinatura `X-Hub-Signature-256`
- **Terraform completo**: Cloud Function, Cloud Scheduler, IAM, Storage, Secret Manager — tudo como código em `ENV-GCP/`
- **Scripts de deploy**: `deploy_terraform.sh` e `create_secret_version.sh` para automação segura
- **Documentação de status**: `ENV-GCP/STATUS.md` com estado atual do projeto

### Changed
- Cloud Function atualizada para v4 com suporte a WhatsApp + Gemini
- Service account `chat-admc-fn-sa` com permissões de Secret Manager
- Leitura de `church-context-gemini.txt` usa caminho absoluto baseado no arquivo (evita falhas por diretório de execução)
- Respostas melhoradas com base em feedback pastoral real

### Fixed
- **Robustez do contexto da igreja**: caminho absoluto para `church-context-gemini.txt` resolve falhas em runtime
- **Fallback amigável para indisponibilidade de IA**: Sara responde mensagem de indisponibilidade em vez de lançar exceção quando `GEMINI_API_KEY` está ausente
- **Observabilidade de secrets**: logs explícitos para falha de acesso ao Secret Manager, ausência de token e status de envio na API da Meta

### Security
- Tokens e secrets movidos para GCP Secret Manager — nenhuma credencial no código
- Histórico do git limpo de credenciais expostas
- Verificação de assinatura HMAC-SHA256 em todos os webhooks recebidos da Meta

---

## [Initial]
- Inicial: adicionados arquivos do projeto e README inicial.

---

Notas:
- Use tags semânticas ao criar releases (`v1.0.0`, `v1.1.0`, ...).
- O arquivo deve ser atualizado antes de cada release com as mudanças relevantes.
