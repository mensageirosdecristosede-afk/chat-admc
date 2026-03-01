# Guia de Configuração do Meta Developer

Este guia fornece instruções passo a passo para configurar a integração com o Meta (WhatsApp, Instagram, Facebook).

## 📋 Pré-requisitos

- Conta Meta Business
- WhatsApp Business Account
- Instagram Business Account
- Facebook Page
- Aplicativo criado no Meta for Developers

## 1️⃣ Criar Aplicativo no Meta for Developers

### Passo 1: Acessar Meta for Developers

1. Acesse [https://developers.facebook.com/](https://developers.facebook.com/)
2. Faça login com sua conta Meta Business
3. Clique em **"My Apps"** > **"Create App"**

### Passo 2: Configurar o Aplicativo

1. Escolha o tipo: **"Business"**
2. Preencha os detalhes:
   - **App Display Name**: Chat ADMC
   - **App Contact Email**: email@igreja-admc.com
   - **Business Portfolio**: Selecione seu portfolio
3. Clique em **"Create App"**

### Passo 3: Adicionar Produtos

No dashboard do app, adicione os seguintes produtos:

#### WhatsApp
1. Clique em **"Add Product"**
2. Selecione **"WhatsApp"** > **"Set Up"**
3. Configure o número de telefone da igreja

#### Messenger
1. Clique em **"Add Product"**
2. Selecione **"Messenger"** > **"Set Up"**
3. Conecte a página do Facebook

#### Instagram
1. Clique em **"Add Product"**
2. Selecione **"Instagram"** > **"Set Up"**
3. Conecte a conta do Instagram

## 2️⃣ Obter Credenciais

### App Secret

1. Vá em **Settings** > **Basic**
2. Clique em **"Show"** ao lado de **"App Secret"**
3. Copie o valor e adicione no `terraform.tfvars`

```hcl
meta_app_secret = "SEU_APP_SECRET_AQUI"
```

### WhatsApp Phone Number ID

1. Vá em **WhatsApp** > **API Setup**
2. Copie o **"Phone number ID"**
3. Adicione no `terraform.tfvars`

```hcl
whatsapp_phone_id = "123456789012345"
```

### Instagram Account ID

1. Vá em **Instagram** > **API Setup**
2. Copie o **"Instagram Business Account ID"**
3. Adicione no `terraform.tfvars`

```hcl
instagram_account_id = "123456789012345"
```

### Facebook Page ID

1. Acesse sua página do Facebook
2. Vá em **About**
3. Role até encontrar **"Page ID"**
4. Adicione no `terraform.tfvars`

```hcl
facebook_page_id = "123456789012345"
```

## 3️⃣ Gerar Token de Acesso Permanente

### Passo 1: Gerar Token Temporário

1. Vá em **Tools** > **Graph API Explorer**
2. Selecione seu aplicativo
3. Adicione as permissões necessárias:
   - `pages_messaging`
   - `pages_manage_metadata`
   - `instagram_basic`
   - `instagram_manage_messages`
   - `whatsapp_business_management`
   - `whatsapp_business_messaging`
4. Clique em **"Generate Access Token"**

### Passo 2: Converter para Token de Longa Duração

Execute o seguinte comando (substitua os valores):

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=SEU_APP_ID&client_secret=SEU_APP_SECRET&fb_exchange_token=TOKEN_TEMPORARIO"
```

O retorno será algo como:

```json
{
  "access_token": "TOKEN_DE_LONGA_DURACAO",
  "token_type": "bearer",
  "expires_in": 5183944
}
```

### Passo 3: Obter Token Permanente (Never Expires)

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/me?access_token=TOKEN_DE_LONGA_DURACAO"
```

Copie o `access_token` e adicione no `terraform.tfvars`:

```hcl
meta_access_token = "SEU_TOKEN_PERMANENTE_AQUI"
```

## 4️⃣ Configurar Webhooks

### Gerar Token de Verificação

Execute no terminal:

```bash
openssl rand -hex 32
```

Adicione o resultado no `terraform.tfvars`:

```hcl
meta_verify_token = "TOKEN_GERADO_AQUI"
```

### Após Deploy do Terraform

Após executar `terraform apply`, você receberá a URL do webhook:

```
webhook_url = "https://xxxxx.execute-api.us-east-1.amazonaws.com/prod/webhook"
```

### Configurar WhatsApp Webhook

1. Vá em **WhatsApp** > **Configuration**
2. Na seção **"Webhook"**, clique em **"Edit"**
3. Preencha:
   - **Callback URL**: URL do webhook (output do Terraform)
   - **Verify Token**: O mesmo token gerado acima
4. Clique em **"Verify and Save"**
5. Inscreva-se nos campos:
   - ✅ messages
   - ✅ messaging_postbacks

### Configurar Instagram Webhook

1. Vá em **Instagram** > **Configuration**
2. Na seção **"Webhooks"**, clique em **"Edit"**
3. Preencha:
   - **Callback URL**: URL do webhook (output do Terraform)
   - **Verify Token**: O mesmo token gerado acima
4. Clique em **"Verify and Save"**
5. Inscreva-se nos campos:
   - ✅ messages
   - ✅ messaging_postbacks
   - ✅ message_reactions

### Configurar Facebook Messenger Webhook

1. Vá em **Messenger** > **Configuration**
2. Na seção **"Webhooks"**, clique em **"Add Callback URL"**
3. Preencha:
   - **Callback URL**: URL do webhook (output do Terraform)
   - **Verify Token**: O mesmo token gerado acima
4. Clique em **"Verify and Save"**
5. Inscreva-se nos campos:
   - ✅ messages
   - ✅ messaging_postbacks
   - ✅ message_deliveries
   - ✅ message_reads

## 5️⃣ Testar a Configuração

### Teste Manual do Webhook

Execute no terminal (substitua os valores):

```bash
curl -X GET "https://SEU_WEBHOOK_URL?hub.mode=subscribe&hub.verify_token=SEU_TOKEN&hub.challenge=test123"
```

Se configurado corretamente, deve retornar: `test123`

### Enviar Mensagem de Teste

1. **WhatsApp**: Envie uma mensagem para o número configurado
2. **Instagram**: Envie uma DM para a conta configurada
3. **Facebook**: Envie uma mensagem via Messenger para a página

### Verificar Logs

```bash
aws logs tail /aws/lambda/chat-admc-webhook-handler --follow
```

## 6️⃣ Modo Produção

### Revisar Aplicativo

Para usar em produção, você precisa enviar o app para revisão:

1. Vá em **App Review** no menu lateral
2. Clique em **"Request Advanced Access"**
3. Solicite as permissões necessárias
4. Preencha os formulários de revisão
5. Aguarde aprovação (pode levar alguns dias)

### Permissões Necessárias

- `pages_messaging` - Enviar mensagens via Facebook
- `instagram_manage_messages` - Mensagens do Instagram
- `whatsapp_business_messaging` - Mensagens do WhatsApp

## 🔒 Segurança

### Validação de Assinatura

O código Lambda já implementa validação de assinatura. Verifique que o `meta_app_secret` está configurado corretamente.

### HTTPS Obrigatório

O Meta exige HTTPS. O API Gateway já fornece isso automaticamente.

### Renovação de Token

Tokens de longa duração expiram após ~60 dias. Configure um lembrete para renovar.

## 🆘 Troubleshooting

### Erro: "Webhook Verification Failed"

- Verifique que o `meta_verify_token` é o mesmo em ambos os lugares
- Confirme que a URL do webhook está correta
- Verifique os logs do CloudWatch

### Erro: "Invalid Signature"

- Verifique que o `meta_app_secret` está correto
- Confirme que o código está validando a assinatura corretamente

### Mensagens não são recebidas

- Verifique que os webhooks estão inscritos nos campos corretos
- Confirme que o token de acesso tem as permissões necessárias
- Verifique os logs do CloudWatch

### Não consigo enviar mensagens

- Confirme que o `meta_access_token` está válido
- Verifique os IDs (phone_id, page_id, etc.)
- Teste com o Graph API Explorer

## 📚 Recursos Adicionais

- [Meta Webhooks Documentation](https://developers.facebook.com/docs/graph-api/webhooks/)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Instagram Messaging API](https://developers.facebook.com/docs/messenger-platform/instagram)
- [Messenger Platform](https://developers.facebook.com/docs/messenger-platform)
- [Access Tokens](https://developers.facebook.com/docs/facebook-login/guides/access-tokens)

---

**Dúvidas?** Consulte a documentação oficial ou abra uma issue no repositório.
