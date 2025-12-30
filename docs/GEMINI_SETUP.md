# 🆓 Configuração Google Gemini API (100% GRATUITO)

## ✨ Por que Gemini?

**Google Gemini API é 100% GRATUITO** com limite generoso:
- ✅ **1.500 requisições por dia**
- ✅ **Sem custo algum**
- ✅ **60 requisições por minuto**
- ✅ **Mesma qualidade do ChatGPT**

Para a Igreja ADMC (estimativa de 100-500 mensagens/mês), isso é **MAIS DO QUE SUFICIENTE!**

---

## 🚀 Como Obter a API Key (5 minutos)

### Passo 1: Acessar Google AI Studio

1. Acesse: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google (pode ser pessoal)

### Passo 2: Criar API Key

1. Clique no botão **"Create API Key"**
2. Selecione um projeto do Google Cloud (ou crie um novo)
3. A chave será gerada automaticamente

**Exemplo de API Key**:
```
AIzaSyD-9tSRv3nJ8x7xKQZqLp4vW2xYzX_AbCd
```

### Passo 3: Copiar a Chave

1. Clique em **"Copy"**
2. Guarde em local seguro

---

## 📝 Configurar no Projeto

### 1. Adicionar no terraform.tfvars

```bash
cd ~/projeto-pessoal/igreja-admc/chat-admc/terraform
nano terraform.tfvars
```

Adicione a linha:
```hcl
gemini_api_key = "AIzaSyD-9tSRv3nJ8x7xKQZqLp4vW2xYzX_AbCd"
```

### 2. Fazer Deploy

```bash
./deploy.sh
```

Pronto! O sistema agora usa Gemini **sem nenhum custo**.

---

## 🧪 Testar a API

### Teste Manual via cURL

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=SUA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Olá, quais os horários dos cultos da igreja?"
      }]
    }]
  }'
```

### Teste via Python

```python
import requests

api_key = "SUA_API_KEY"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Olá! Como você pode me ajudar?"
        }]
    }]
}

response = requests.post(url, json=payload)
print(response.json())
```

---

## 📊 Limites do Free Tier

| Recurso | Limite | Suficiente? |
|---------|--------|-------------|
| **Requisições/dia** | 1.500 | ✅ Sim (50x mais que necessário) |
| **Requisições/minuto** | 60 | ✅ Sim |
| **Tokens/requisição** | 30.000 | ✅ Sim |
| **Custo** | $0.00 | ✅ 100% Grátis |

**Para 500 mensagens/mês**: Usa apenas **17 req/dia** (1% do limite!)

---

## 🔒 Segurança da API Key

### ✅ FAÇA:
- Mantenha a chave em variável de ambiente
- Use SSM Parameter Store (já configurado)
- Não commite no Git (já protegido por .gitignore)
- Regenere se comprometida

### ❌ NÃO FAÇA:
- Compartilhar publicamente
- Commitar no código
- Enviar por email/WhatsApp
- Usar em frontend (cliente)

---

## 🔄 Regenerar API Key

Se a chave for comprometida:

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Clique nos 3 pontos da chave atual
3. Clique em **"Delete"**
4. Crie uma nova chave
5. Atualize o `terraform.tfvars`
6. Faça deploy novamente

---

## 📈 Monitorar Uso

### Via Google Cloud Console

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Vá em **APIs & Services** > **Dashboard**
3. Selecione **"Generative Language API"**
4. Veja estatísticas de uso

### Alertas Recomendados

Configure alertas se uso > 1000 req/dia:
1. Console > APIs & Services > Quotas
2. Selecione a API
3. Configure alerta de quota

---

## ❓ FAQ

### P: Preciso cadastrar cartão de crédito?
**R**: Não! O Gemini API é 100% gratuito, sem necessidade de cartão.

### P: Tem tempo de expiração?
**R**: Não, o free tier é permanente.

### P: E se ultrapassar 1500 req/dia?
**R**: A API retorna erro 429 (Too Many Requests). O sistema usa resposta fallback.

### P: Posso usar múltiplas API keys?
**R**: Sim, mas não é necessário. 1500 req/dia é mais que suficiente.

### P: Precisa de conta Google Workspace?
**R**: Não, conta Google pessoal funciona perfeitamente.

### P: Funciona no Brasil?
**R**: Sim! Funciona em todos os países.

---

## 🆚 Comparação: Gemini vs Bedrock

| Feature | Google Gemini | AWS Bedrock |
|---------|---------------|-------------|
| **Custo** | $0.00 | ~$2/mês |
| **Limite diário** | 1500 req | Ilimitado (mas pago) |
| **Qualidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Velocidade** | 2-5s | 2-5s |
| **Setup** | 5 min | 10 min |
| **Requer cartão** | ❌ Não | ✅ Sim |

**Veredito para POC**: Gemini é perfeito! 🎉

---

## 🎯 Outras Alternativas Gratuitas

Se precisar de mais capacidade ou alternativas:

### 1. Groq (Meta Llama)
- **URL**: https://console.groq.com/
- **Modelo**: Llama 3
- **Limite**: 10.000 req/dia
- **Velocidade**: Ultra rápida
- **Custo**: Grátis

### 2. Hugging Face
- **URL**: https://huggingface.co/
- **Modelos**: Vários (Mistral, Llama, etc)
- **Limite**: ~1000 req/dia
- **Custo**: Grátis

### 3. Cohere
- **URL**: https://cohere.com/
- **Modelo**: Command
- **Limite**: 1000 req/mês
- **Custo**: Grátis

---

## 🛠️ Troubleshooting

### Erro: "API Key inválida"
```bash
# Verificar se a chave está correta
echo $GEMINI_API_KEY

# Testar diretamente
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=SUA_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"teste"}]}]}'
```

### Erro: "429 Too Many Requests"
- Você atingiu o limite de 1500 req/dia
- Aguarde 24h para reset
- Sistema usa resposta fallback automaticamente

### Erro: "403 Forbidden"
- API não está ativada no projeto
- Acesse Google Cloud Console > APIs & Services
- Ative "Generative Language API"

---

## 📞 Suporte

### Documentação Oficial
- [Google AI Studio](https://ai.google.dev/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [API Reference](https://ai.google.dev/api/python/google/generativeai)

### Community
- [Google AI Discord](https://discord.gg/google-ai)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-gemini)

---

## ✅ Checklist Final

- [ ] API Key obtida do Google AI Studio
- [ ] Adicionada ao terraform.tfvars
- [ ] Deploy realizado com sucesso
- [ ] Teste de mensagem funcionando
- [ ] Logs verificados no CloudWatch
- [ ] Monitoramento configurado

---

**🎉 Parabéns! Agora você tem IA 100% GRATUITA! 🙏**

**Custo total do projeto**: **$0.00/mês** ✨

---

**Última atualização**: 30/12/2024  
**Autor**: Sistema Chat ADMC
