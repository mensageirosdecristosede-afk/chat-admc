# Infraestrutura GCP - Chat ADMC

## Componentes Criados

- **Cloud Storage Bucket**: Armazena arquivos e código da função.
- **Cloud Function (Python)**: Endpoint HTTP para processamento.
- **Artifact Registry**: Usado para build e cache de imagens.
- **Permissões**: Service accounts ajustadas para build, logs e deploy.

## Arquitetura

```
Usuário → Cloud Function (HTTP) → Cloud Storage
           ↑
         Cloud Build (deploy)
           ↑
     Artifact Registry (cache)
```

## Como testar

1. Após `terraform apply`, pegue o output `function_url`.
2. Faça uma requisição HTTP:
   ```
   curl https://<function_url>
   ```
   Deve retornar: `Hello from Chat ADMC Cloud Function!`

## Próximos passos

- Personalizar o código da Cloud Function conforme sua lógica.
- Integrar com Google Gemini API (aproveitando o free tier).
- Monitorar logs e permissões.
- Garantir que não há custos: use apenas recursos do free tier, evite uploads grandes e execuções excessivas.

## Revisão de custos (Free Tier)

- **Cloud Functions**: 2 milhões de invocações/mês, 400 mil GB-segundos/mês.
- **Cloud Storage**: 5 GB/mês.
- **Artifact Registry**: 0,5 GB/mês.
- **Cloud Build**: 120 minutos/mês.

> Se exceder esses limites, haverá cobrança. Monitore pelo console GCP (Billing).

## Checklist de monitoramento

- [ ] Verificar quotas e limites no console GCP.
- [ ] Configurar alertas de orçamento.
- [ ] Monitorar logs de invocações e uso.
- [ ] Evitar uploads e execuções fora do free tier.

---

**Qualquer dúvida ou erro, envie o log para análise!**


## Configurar `GEMINI_API_KEY` no Secret Manager (recomendado)

Siga estes passos para criar o secret com a chave da API Gemini e conceder acesso à service account usada pela Cloud Function.

1. Defina o projeto GCP (substitua `MY_PROJECT`):

```bash
gcloud config set project MY_PROJECT
```


2. Crie o recurso do Secret Manager via Terraform (o `secret` será criado sem versão) e depois adicione a versão com o valor sensível usando `gcloud`:

```bash
# cria apenas o recurso secret (sem versão) via Terraform
cd ENV-GCP
terraform init
terraform apply -var="project_id=MY_PROJECT" -var="bucket_name=MY_BUCKET" --auto-approve

# adicione a versão contendo o valor sensível (substitua YOUR_GEMINI_KEY)
printf '%s' "YOUR_GEMINI_KEY" | gcloud secrets versions add GEMINI_API_KEY --data-file=-
```

3. Conceda à service account da Cloud Function permissão para acessar o secret (substitua `SERVICE_ACCOUNT_EMAIL`):

```bash
gcloud secrets add-iam-policy-binding GEMINI_API_KEY \
  --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
  --role="roles/secretmanager.secretAccessor"
```

Exemplo (para a service account declarada no `cloudfunction.tf`):

```bash
gcloud secrets add-iam-policy-binding GEMINI_API_KEY \
  --member="serviceAccount:chat-bot-admc@MY_PROJECT.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

4. Depois de criar o secret e configurar IAM, faça o deploy (o `cloudfunction.tf` já define `GEMINI_SECRET_NAME="GEMINI_API_KEY"` como variável de ambiente):

```bash
cd ENV-GCP
zip -r function-source.zip main.py requirements.txt church-context-gemini.txt
terraform init
terraform apply --auto-approve
```

Observação: a função lê o nome do secret via `GEMINI_SECRET_NAME` e acessa o valor em runtime pelo Secret Manager; não é necessário inserir a chave diretamente como env var.
