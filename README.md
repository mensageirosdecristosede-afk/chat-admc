# Chat ADMC - Sistema de Atendimento Multi-Canal

Sistema de chat automatizado com IA para atendimento via WhatsApp, Instagram e Facebook Messenger para a Igreja ADMC.

## 🏗️ Arquitetura

A solução utiliza infraestrutura serverless na AWS (Free Tier) com integração Meta Business API:

- **AWS Lambda**: Processamento de mensagens e lógica de IA
- **Amazon API Gateway**: Endpoint para webhooks do Meta
- **Amazon S3**: Armazenamento de conversas e dados de treinamento
- **Amazon Bedrock**: IA generativa para respostas humanizadas (Claude 3)
- **Meta Business API**: Integração com WhatsApp, Instagram e Facebook

## 📋 Pré-requisitos

1. **Conta AWS** com credenciais configuradas
2. **Meta Business Account** com:
   - WhatsApp Business API
   - Instagram Business Account
   - Facebook Page
3. **Ferramentas necessárias**:
   - Terraform >= 1.0
   - Python 3.11+
   - AWS CLI
   - Git

## 🚀 Instalação e Deploy

### 1. Clone o repositório

```bash
git clone <repository-url>
cd chat-admc
```

### 2. Configure as variáveis Terraform

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edite `terraform.tfvars` com suas informações:

```hcl
# Informações AWS
aws_region     = "us-east-1"
project_name   = "chat-admc"
environment    = "prod"

# Informações Meta
meta_verify_token     = "seu-token-de-verificacao-seguro"
meta_app_secret       = "seu-app-secret-do-meta"
whatsapp_phone_id     = "seu-whatsapp-phone-number-id"
instagram_account_id  = "seu-instagram-account-id"
facebook_page_id      = "seu-facebook-page-id"
meta_access_token     = "seu-token-de-acesso-permanente"

# Tags
tags = {
  Project     = "ChatADMC"
  Environment = "Production"
  ManagedBy   = "Terraform"
}
```

### 3. Deploy da Infraestrutura

```bash
cd terraform

# Inicializar Terraform
terraform init

# Verificar o plano de execução
terraform plan

# Aplicar as mudanças
terraform apply
```

Anote a URL do webhook que será exibida no output.

### 4. Configurar Webhooks no Meta

#### WhatsApp Business API

1. Acesse [Meta for Developers](https://developers.facebook.com/)
2. Vá para seu App > WhatsApp > Configuration
3. Configure o webhook:
   - **Callback URL**: URL do API Gateway (output do Terraform)
   - **Verify Token**: Mesmo valor de `meta_verify_token`
   - **Webhook Fields**: `messages`, `messaging_postbacks`

#### Instagram

1. Acesse seu App > Instagram > Configuration
2. Configure o webhook:
   - **Callback URL**: URL do API Gateway (output do Terraform)
   - **Verify Token**: Mesmo valor de `meta_verify_token`
   - **Webhook Fields**: `messages`, `messaging_postbacks`

#### Facebook Messenger

1. Acesse seu App > Messenger > Configuration
2. Configure o webhook:
   - **Callback URL**: URL do API Gateway (output do Terraform)
   - **Verify Token**: Mesmo valor de `meta_verify_token`
   - **Webhook Fields**: `messages`, `messaging_postbacks`

### 5. Testar a Integração

Envie uma mensagem de teste pelo WhatsApp, Instagram ou Facebook para o número/conta da igreja.

## 🤖 Treinamento da IA

### Upload de Documentos de Treinamento

1. Prepare documentos com informações da igreja (formato .txt, .pdf ou .json)
2. Faça upload para o bucket S3:

```bash
aws s3 cp documentos/ s3://chat-admc-knowledge-base/ --recursive
```

### Estrutura de Documentos Recomendada

```
knowledge-base/
├── horarios.txt          # Horários de cultos e eventos
├── localizacao.txt       # Endereço e como chegar
├── ministerios.txt       # Informações sobre ministérios
├── contatos.txt          # Contatos de lideranças
├── doutrina.txt          # Informações doutrinárias
└── eventos.txt           # Próximos eventos
```

## 📊 Monitoramento

### CloudWatch Logs

```bash
# Ver logs da Lambda
aws logs tail /aws/lambda/chat-admc-webhook-handler --follow
```

### Métricas

Acesse o CloudWatch Dashboard:
- Invocações da Lambda
- Duração das execuções
- Erros e throttling

## 💰 Custos (Free Tier)

- **Lambda**: 1M requisições/mês grátis
- **API Gateway**: 1M requisições/mês grátis
- **S3**: 5GB armazenamento grátis
- **Bedrock**: Verificar pricing (não tem free tier permanente, mas tem trial)

**Estimativa mensal**: $0 - $5 (dependendo do volume)

## 🔒 Segurança

- Credenciais armazenadas em AWS Systems Manager Parameter Store
- Validação de assinatura dos webhooks Meta
- HTTPS obrigatório para todos os endpoints
- Princípio de menor privilégio para IAM roles

## 🛠️ Desenvolvimento Local

### Testar Lambda Localmente

```bash
cd lambda
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Testar função
python -c "from webhook_handler import lambda_handler; print(lambda_handler({}, {}))"
```

## 📚 Documentação Adicional

- [Meta Webhooks Documentation](https://developers.facebook.com/docs/graph-api/webhooks/)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

## 🤝 Contribuindo

Para contribuir com o projeto:

1. Crie uma branch para sua feature
2. Faça commit das mudanças
3. Abra um Pull Request

## 📞 Suporte

Para questões técnicas, abra uma issue no repositório.

---

**Desenvolvido com ❤️ para a Igreja ADMC**
