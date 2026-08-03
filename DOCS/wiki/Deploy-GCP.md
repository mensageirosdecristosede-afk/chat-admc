# Deploy GCP — Cloud Function + Terraform

## Pré-requisitos

- `gcloud` CLI configurado e autenticado
- `terraform` >= 1.0
- Acesso ao projeto GCP `chat-bot-admc`
- Roles necessárias na conta GCP:
  - `roles/cloudfunctions.admin`
  - `roles/cloudscheduler.admin`
  - `roles/iam.serviceAccountUser`
  - `roles/storage.admin`
  - `roles/secretmanager.admin`
  - `roles/resourcemanager.projectIamAdmin`

---

## Deploy Completo (Terraform)

```bash
cd ENV-GCP/

# 1. Inicializar Terraform
terraform init

# 2. Revisar o plano
terraform plan

# 3. Aplicar
terraform apply
```

Ou usar o script auxiliar:

```bash
cd ENV-GCP/scripts/
./deploy_terraform.sh
```

---

## Deploy Rápido (apenas código da função)

Para publicar apenas mudanças em `main.py` sem recriar infra:

```bash
cd ENV-GCP/
zip -r function-source.zip main.py requirements.txt church-context-gemini.txt

gcloud functions deploy chat-admc-handler \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1 \
  --project chat-bot-admc \
  --source .
```

---

## Gerenciar Secrets

### Criar/atualizar um secret

```bash
cd ENV-GCP/scripts/
./create_secret_version.sh
```

Ou manualmente:

```bash
# Criar nova versão de um secret existente
echo -n "VALOR_DO_SECRET" | gcloud secrets versions add NOME_DO_SECRET \
  --data-file=- \
  --project chat-bot-admc
```

### Secrets necessários

| Nome | Descrição |
|---|---|
| `GEMINI_API_KEY` | Chave da API Google Gemini (Google AI Studio) |
| `WHATSAPP_TOKEN` | Token do System User "deploy-whatsapp" (Meta) |
| `META_APP_SECRET` | App Secret do app "Chat ADMC" (Meta Developer Console) |

---

## Variáveis Terraform

Edite `ENV-GCP/terraform.tfvars` antes de aplicar:

```hcl
project_id = "chat-bot-admc"
region     = "us-central1"
# ... demais variáveis
```

> **Atenção**: nunca commitar valores de secrets em `terraform.tfvars`.

---

## Verificar Deploy

```bash
# Ver logs em tempo real
gcloud functions logs read chat-admc-handler \
  --region us-central1 \
  --project chat-bot-admc \
  --limit 50

# Testar endpoint
curl -X GET "https://us-central1-chat-bot-admc.cloudfunctions.net/chat-admc-handler?hub.mode=subscribe&hub.verify_token=admc-verify-2026&hub.challenge=test123"
# Resposta esperada: test123
```

---

## Rollback

```bash
# Listar versões anteriores da função
gcloud functions describe chat-admc-handler --region us-central1 --project chat-bot-admc

# Para reverter: redeploy do commit anterior via git
git checkout <commit-anterior> -- ENV-GCP/main.py ENV-GCP/requirements.txt
# Então fazer deploy manual ou via Terraform
```
