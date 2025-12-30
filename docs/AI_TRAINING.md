# Guia de Treinamento da IA

Este guia explica como treinar e customizar a IA do chatbot para responder adequadamente sobre a Igreja ADMC.

## 📚 Base de Conhecimento

A IA utiliza documentos armazenados no S3 como base de conhecimento. O principal arquivo é `knowledge-base/church-context.txt`.

## 🎯 Estrutura do Contexto

### 1. Informações Básicas

```txt
Igreja ADMC - Assembleia de Deus Ministério Caná

INFORMAÇÕES GERAIS:
- Nome completo da igreja
- Denominação
- Missão e visão
- História resumida
```

### 2. Horários e Programação

```txt
HORÁRIOS DE CULTOS:
- Terça-feira: 19h30 - Culto de Doutrina
- Quinta-feira: 19h30 - Culto de Oração
- Sexta-feira: 19h30 - Culto de Jovens
- Domingo: 09h00 - Escola Bíblica Dominical
- Domingo: 19h00 - Culto de Celebração

PROGRAMAÇÕES ESPECIAIS:
- Primeira sexta-feira do mês: Vigília
- Último domingo do mês: Santa Ceia
```

### 3. Localização e Contato

```txt
LOCALIZAÇÃO:
Endereço: Rua [Nome], nº [Número]
Bairro: [Bairro]
Cidade: [Cidade] - [Estado]
CEP: [CEP]

COMO CHEGAR:
- De ônibus: Linhas [números]
- De carro: [Referências]
- Estacionamento: [Informações]

CONTATOS:
- Telefone: (XX) XXXX-XXXX
- WhatsApp: (XX) XXXXX-XXXX
- Email: contato@igrejadmc.com.br
- Site: www.igrejadmc.com.br
- Instagram: @igrejadmc
- Facebook: /igrejadmc
```

### 4. Ministérios

```txt
MINISTÉRIOS:

Ministério de Louvor:
- Descrição: Conduz a adoração nos cultos
- Responsável: [Nome]
- Contato: [Telefone/Email]
- Como participar: Audição às [dia/hora]

Ministério Infantil:
- Descrição: Cuida das crianças durante os cultos
- Idade: 0 a 12 anos
- Responsável: [Nome]
- Atividades: EBD, eventos especiais

[... outros ministérios ...]
```

### 5. Eventos

```txt
PRÓXIMOS EVENTOS:
- [Data]: Congresso de Jovens
- [Data]: Retiro Espiritual
- [Data]: Conferência de Mulheres

EVENTOS ANUAIS:
- Janeiro: Jejum e Oração (21 dias)
- Abril: Páscoa
- Junho: Festa Junina
- Dezembro: Natal
```

### 6. Perguntas Frequentes

```txt
PERGUNTAS FREQUENTES:

P: Como me tornar membro da igreja?
R: Você pode participar do curso de membros que acontece [quando]. 
   Após concluir, será batizado e receberá o certificado de membro.

P: Preciso me vestir de alguma forma especial?
R: Não há código de vestimenta. Vista-se confortavelmente e com modéstia.

P: Tem estacionamento?
R: Sim, temos estacionamento gratuito com [X] vagas.

P: Tem atividades para crianças?
R: Sim, temos ministério infantil durante todos os cultos.

[... outras perguntas ...]
```

### 7. Doutrinas e Crenças

```txt
DOUTRINAS:
- Cremos na Bíblia como Palavra de Deus
- Cremos na Trindade: Pai, Filho e Espírito Santo
- Cremos na salvação pela graça mediante a fé
- Cremos no batismo por imersão
- Cremos na santa ceia
- Cremos no batismo no Espírito Santo
- Cremos na volta de Jesus

VERSÍCULOS IMPORTANTES:
- João 3:16 - "Porque Deus amou o mundo..."
- Atos 2:38 - "Arrependei-vos e cada um seja batizado..."
- Efésios 2:8-9 - "Porque pela graça sois salvos..."
```

## 📝 Como Atualizar o Contexto

### Método 1: Via AWS CLI

```bash
# Edite o arquivo localmente
nano church-context.txt

# Faça upload para o S3
aws s3 cp church-context.txt s3://chat-admc-data-[ACCOUNT_ID]/knowledge-base/
```

### Método 2: Via Console AWS

1. Acesse o S3 no console AWS
2. Navegue até o bucket `chat-admc-data-[ACCOUNT_ID]`
3. Entre na pasta `knowledge-base/`
4. Clique em **Upload** e selecione o arquivo

### Método 3: Editar Diretamente no Terraform

Edite o arquivo `terraform/s3.tf` e execute `terraform apply`.

## 🤖 Personalização do Comportamento

### System Prompt

O comportamento da IA é definido no `system_prompt` em `lambda/webhook_handler.py`:

```python
system_prompt = f"""Você é um assistente virtual da Igreja ADMC.
Seu papel é ajudar as pessoas com informações sobre a igreja de forma educada.

Contexto da Igreja:
{church_context}

Diretrizes:
- Seja sempre educado e acolhedor
- Use linguagem simples e amigável
- Se não souber algo, seja honesto
- Mantenha respostas concisas (máximo 300 palavras)
- Inclua versículos bíblicos quando apropriado
- Convide as pessoas para conhecer a igreja
"""
```

### Customizações Sugeridas

#### Tom de Voz

Para um tom mais formal:
```python
- Seja sempre educado e respeitoso
- Use linguagem formal e clara
- Evite gírias e informalidades
```

Para um tom mais casual:
```python
- Seja amigável e acolhedor
- Use uma linguagem próxima e calorosa
- Pode usar emojis moderadamente 😊
```

#### Tipos de Resposta

Para respostas mais curtas:
```python
- Mantenha respostas objetivas (máximo 150 palavras)
- Use bullets quando listar informações
```

Para respostas mais detalhadas:
```python
- Forneça explicações completas
- Inclua contexto histórico quando relevante
- Sugira recursos adicionais
```

## 📊 Análise de Conversas

As conversas são salvas em `s3://[bucket]/conversations/`. Use-as para:

### 1. Identificar Perguntas Comuns

```bash
# Baixar conversas do último mês
aws s3 sync s3://chat-admc-data-[ACCOUNT]/conversations/ ./conversations/ \
  --exclude "*" --include "2024/12/*"

# Analisar perguntas frequentes
grep -r "user_message" conversations/ | sort | uniq -c | sort -rn | head -20
```

### 2. Melhorar Respostas

Revise as conversas para identificar:
- Perguntas que a IA não soube responder
- Respostas que podem ser melhoradas
- Novos tópicos para adicionar ao contexto

### 3. Monitorar Qualidade

Verifique regularmente:
- Taxa de respostas "não sei"
- Feedback dos usuários
- Conversas que exigiram intervenção humana

## 🔧 Ajustes Finos

### Temperatura

No código Lambda, ajuste a `temperature` (0 a 1):

```python
payload = {
    "temperature": 0.7,  # Padrão: criativo mas consistente
    # ...
}
```

- **0.0-0.3**: Respostas mais determinísticas e precisas
- **0.4-0.7**: Equilíbrio entre criatividade e precisão
- **0.8-1.0**: Mais criativo e variado

### Max Tokens

Ajuste `max_tokens` para controlar o tamanho da resposta:

```python
payload = {
    "max_tokens": 500,  # Padrão
    # ...
}
```

### Modelo Bedrock

Altere o modelo conforme necessário:

```python
# Mais econômico
modelId='anthropic.claude-3-haiku-20240307-v1:0'

# Mais inteligente (mais caro)
modelId='anthropic.claude-3-sonnet-20240229-v1:0'
```

## 📚 Documentos Adicionais

### Estrutura Recomendada

```
knowledge-base/
├── church-context.txt        # Contexto principal (obrigatório)
├── eventos.txt               # Lista detalhada de eventos
├── ministerios.txt           # Descrição completa dos ministérios
├── doutrina.txt             # Doutrinas e crenças
├── historia.txt             # História da igreja
├── lideranca.txt            # Liderança e contatos
└── faq.txt                  # Perguntas frequentes expandidas
```

### Como Adicionar Múltiplos Documentos

Modifique `load_church_context()` em `webhook_handler.py`:

```python
def load_church_context() -> str:
    context_files = [
        'church-context.txt',
        'eventos.txt',
        'ministerios.txt',
        'faq.txt'
    ]
    
    combined_context = []
    
    for filename in context_files:
        try:
            response = s3_client.get_object(
                Bucket=BUCKET_NAME,
                Key=f'knowledge-base/{filename}'
            )
            content = response['Body'].read().decode('utf-8')
            combined_context.append(content)
        except:
            logger.warning(f"Arquivo {filename} não encontrado")
    
    return '\n\n'.join(combined_context)
```

## 🎓 Boas Práticas

1. **Atualize regularmente**: Mantenha informações sempre atualizadas
2. **Seja específico**: Quanto mais detalhes, melhores as respostas
3. **Teste mudanças**: Sempre teste após adicionar novo conteúdo
4. **Monitore feedback**: Ajuste baseado no feedback dos usuários
5. **Backup**: Mantenha backup dos contextos em Git

## 🔄 Processo de Atualização

```bash
# 1. Editar contexto localmente
nano knowledge-base/church-context.txt

# 2. Testar localmente (opcional)
python test_context.py

# 3. Fazer upload para S3
aws s3 cp knowledge-base/ s3://chat-admc-data-[ACCOUNT]/knowledge-base/ --recursive

# 4. Monitorar logs
aws logs tail /aws/lambda/chat-admc-webhook-handler --follow

# 5. Testar com mensagens reais
# Envie mensagens de teste via WhatsApp/Instagram/Facebook
```

---

**Lembre-se**: A qualidade das respostas depende diretamente da qualidade do contexto fornecido!
