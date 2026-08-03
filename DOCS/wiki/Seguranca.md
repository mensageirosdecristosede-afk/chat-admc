# Segurança

## Princípios

- **Zero secrets no código**: nenhuma credencial, token ou chave deve estar em arquivos commitados
- **Secret Manager como fonte única da verdade**: todos os secrets em runtime vêm do GCP Secret Manager
- **Validação de origem**: todo webhook da Meta é validado com HMAC-SHA256 antes de qualquer processamento
- **Princípio do menor privilégio**: a service account `chat-admc-fn-sa` tem apenas os papéis mínimos necessários

---

## Service Account

**Nome**: `chat-admc-fn-sa@chat-bot-admc.iam.gserviceaccount.com`

| Papel | Motivo |
|---|---|
| `roles/logging.logWriter` | Escrever logs no Cloud Logging |
| `roles/storage.objectViewer` | Ler arquivos do Cloud Storage |
| `roles/secretmanager.secretAccessor` | Ler secrets do Secret Manager |

---

## Secrets Gerenciados

| Secret | Como é usado |
|---|---|
| `GEMINI_API_KEY` | Autenticar chamadas para Gemini API |
| `WHATSAPP_TOKEN` | Autenticar envio de mensagens via WhatsApp Cloud API |
| `META_APP_SECRET` | Validar assinatura HMAC-SHA256 dos webhooks da Meta |

### Rotação de Credenciais

```bash
# Exemplo: rotacionar WHATSAPP_TOKEN
echo -n "NOVO_TOKEN_AQUI" | gcloud secrets versions add WHATSAPP_TOKEN \
  --data-file=- \
  --project chat-bot-admc

# Verificar versões ativas
gcloud secrets versions list WHATSAPP_TOKEN --project chat-bot-admc
```

Após criar nova versão, **desativar** a versão antiga:

```bash
gcloud secrets versions disable VERSAO_ANTIGA \
  --secret WHATSAPP_TOKEN \
  --project chat-bot-admc
```

---

## Validação de Webhook

```python
# Lógica implementada em main.py
import hmac, hashlib

def is_valid_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

- Usa `hmac.compare_digest` para evitar timing attacks
- Retorna `403` imediatamente se inválido, sem processar o payload

---

## Histórico do Git

O repositório passou por limpeza de histórico para remover credenciais expostas em commits anteriores. Qualquer credencial que esteve no histórico deve ser considerada **comprometida e rotacionada**.

---

## Checklist de Segurança para Novos Deploys

- [ ] Nenhum secret em `terraform.tfvars` commitado
- [ ] `terraform.tfvars` está no `.gitignore`
- [ ] Secrets criados/atualizados no Secret Manager antes do deploy
- [ ] Service account com papéis mínimos necessários
- [ ] Webhook verify token configurado corretamente na Meta
- [ ] `META_APP_SECRET` atualizado se houve rotação no app Meta
