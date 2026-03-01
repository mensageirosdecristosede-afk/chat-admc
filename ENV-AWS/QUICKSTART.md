# Guia de Deploy Rápido

## 🚀 Deploy em 10 Minutos

### Passo 1: Clonar e Configurar (2 min)

```bash
cd chat-admc/terraform
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars  # Editar com suas informações
```

### Passo 2: Configurar AWS Credentials (1 min)

```bash
export AWS_ACCESS_KEY_ID="AKIAS4SEB5ASXHGCBIUT"
export AWS_SECRET_ACCESS_KEY="sua_secret_key"
export AWS_DEFAULT_REGION="us-east-1"
```

### Passo 3: Deploy (5 min)

```bash
./deploy.sh
```

### Passo 4: Configurar Meta (2 min)

1. Copie a **webhook_url** do output do Terraform
2. Configure em Meta Developer Console
3. Teste enviando mensagem

## ✅ Checklist Pré-Deploy

- [ ] Conta AWS criada e com credenciais
- [ ] Conta Meta Business configurada
- [ ] WhatsApp Business API ativo
- [ ] Instagram Business conectado
- [ ] Facebook Page configurada
- [ ] Terraform instalado
- [ ] Python 3.11+ instalado
- [ ] AWS CLI instalado

## 📝 Informações Necessárias

### AWS
```
AWS_ACCESS_KEY_ID=AKIAS4SEB5ASXHGCBIUT
AWS_SECRET_ACCESS_KEY=[SUA_SECRET_KEY]
AWS_REGION=us-east-1
```

### Meta
```
meta_verify_token=[GERAR COM: openssl rand -hex 32]
meta_app_secret=[DO META DEVELOPER]
whatsapp_phone_id=[DO META DEVELOPER]
instagram_account_id=[DO META DEVELOPER]
facebook_page_id=[DA SUA PÁGINA]
meta_access_token=[GERAR TOKEN PERMANENTE]
```

## 🧪 Teste Rápido

```bash
# 1. Testar verificação webhook
curl -X GET "https://SEU_WEBHOOK_URL?hub.mode=subscribe&hub.verify_token=SEU_TOKEN&hub.challenge=test"

# 2. Ver logs
aws logs tail /aws/lambda/chat-admc-webhook-handler --follow

# 3. Enviar mensagem teste
# Via WhatsApp/Instagram/Facebook
```

## 🆘 Solução de Problemas

### Erro: "Webhook verification failed"
```bash
# Verificar token
terraform output
# Deve coincidir com o configurado no Meta
```

### Erro: "Lambda timeout"
```bash
# Aumentar timeout
# Em lambda.tf: timeout = 120
terraform apply
```

### Erro: "Bedrock access denied"
```bash
# Ativar Bedrock na região
aws bedrock list-foundation-models --region us-east-1
# Solicitar acesso se necessário
```

## 📊 Monitoramento

```bash
# Ver invocações Lambda
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=chat-admc-webhook-handler \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-31T23:59:59Z \
  --period 3600 \
  --statistics Sum

# Ver custos estimados
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

## 🗑️ Destruir Infraestrutura

```bash
cd terraform
./destroy.sh
```

---

## 📞 Contatos Úteis

- **AWS Support**: https://console.aws.amazon.com/support
- **Meta Support**: https://developers.facebook.com/support
- **Documentação**: Ver pasta `/docs`
