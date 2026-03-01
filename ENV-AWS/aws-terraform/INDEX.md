# 📑 ÍNDICE DO PROJETO - Chat ADMC

Navegação rápida por todos os recursos do projeto.

---

## 🚀 COMEÇAR AQUI

**Novo no projeto?** Comece por aqui:

1. 📄 [README.md](README.md) - Visão geral completa do projeto
2. 📄 [RESUMO.md](RESUMO.md) - Resumo executivo técnico
3. 📄 [PROXIMOS-PASSOS.md](PROXIMOS-PASSOS.md) - Guia passo a passo detalhado
4. 📄 [QUICKSTART.md](QUICKSTART.md) - Deploy rápido em 10 minutos

---

## 📚 DOCUMENTAÇÃO

### Guias Principais
- [README.md](README.md) - Documentação principal
- [RESUMO.md](RESUMO.md) - Resumo executivo
- [QUICKSTART.md](QUICKSTART.md) - Deploy rápido
- [PROXIMOS-PASSOS.md](PROXIMOS-PASSOS.md) - Guia completo

### Documentação Técnica Detalhada
- [docs/META_SETUP.md](docs/META_SETUP.md) - Configuração Meta Developer
- [docs/GEMINI_SETUP.md](docs/GEMINI_SETUP.md) - **Configuração Google Gemini (IA 100% Grátis)**
- [docs/AI_TRAINING.md](docs/AI_TRAINING.md) - Treinamento da IA
- [docs/CUSTOS.md](docs/CUSTOS.md) - Análise de custos e otimização
- [docs/arquitetura-chat-admc.drawio](docs/arquitetura-chat-admc.drawio) - Diagrama de arquitetura

### Templates e Exemplos
- [docs/church-context-template.txt](docs/church-context-template.txt) - Template de contexto
- [terraform/terraform.tfvars.example](terraform/terraform.tfvars.example) - Exemplo de configuração

### Segurança (NÃO COMMITADO)
- `ACESSOS-PRIVADO.md` - Credenciais AWS e Meta (local only)

---

## 💻 CÓDIGO

### Lambda Function
- [lambda/webhook_handler.py](lambda/webhook_handler.py) - Handler principal (320 linhas)
- [lambda/requirements.txt](lambda/requirements.txt) - Dependências Python

### Testes
- [test_local.py](test_local.py) - Testes locais da função Lambda

---

## 🏗️ INFRAESTRUTURA (Terraform)

### Configuração Base
- [terraform/provider.tf](terraform/provider.tf) - Provider AWS
- [terraform/variables.tf](terraform/variables.tf) - Definição de variáveis
- [terraform/outputs.tf](terraform/outputs.tf) - Outputs do Terraform

### Recursos AWS
- [terraform/lambda.tf](terraform/lambda.tf) - Lambda Function e Layer
- [terraform/api_gateway.tf](terraform/api_gateway.tf) - API Gateway REST
- [terraform/s3.tf](terraform/s3.tf) - S3 Bucket e objetos
- [terraform/iam.tf](terraform/iam.tf) - IAM Roles e SSM Parameters

### Scripts de Automação
- [terraform/deploy.sh](terraform/deploy.sh) - Deploy completo
- [terraform/destroy.sh](terraform/destroy.sh) - Destruição de recursos
- [terraform/create_layer.sh](terraform/create_layer.sh) - Criação do Lambda Layer

---

## 📖 GUIAS POR TAREFA

### Fazer Deploy

**Primeira vez:**
1. Leia [PROXIMOS-PASSOS.md](PROXIMOS-PASSOS.md)
2. Configure [terraform/terraform.tfvars.example](terraform/terraform.tfvars.example)
3. Execute `terraform/deploy.sh`
4. Siga [docs/META_SETUP.md](docs/META_SETUP.md)

**Deploy rápido:**
1. Leia [QUICKSTART.md](QUICKSTART.md)
2. Execute comandos listados

### Configurar Meta

1. Leia [docs/META_SETUP.md](docs/META_SETUP.md)
2. Obtenha credenciais Meta
3. Configure webhooks
4. Teste integração

### Configurar Gemini (IA Gratuita)

1. Leia [docs/GEMINI_SETUP.md](docs/GEMINI_SETUP.md)
2. Obtenha API Key gratuita (5 min)
3. Configure no terraform.tfvars
4. Teste respostas da IA

### Treinar IA

1. Leia [docs/AI_TRAINING.md](docs/AI_TRAINING.md)
2. Edite [docs/church-context-template.txt](docs/church-context-template.txt)
3. Faça upload para S3
4. Teste respostas

### Monitorar Custos

1. Leia [docs/CUSTOS.md](docs/CUSTOS.md)
2. Configure AWS Budgets
3. Monitore CloudWatch
4. Otimize se necessário

### Troubleshooting

**Logs:**
```bash
aws logs tail /aws/lambda/chat-admc-webhook-handler --follow
```

**Documentação:**
- [README.md](README.md) - Seção Troubleshooting
- [docs/META_SETUP.md](docs/META_SETUP.md) - Seção Troubleshooting

---

## 🔍 BUSCA RÁPIDA

### Por Assunto

**AWS:**
- Terraform: `terraform/`
- Lambda: [lambda/webhook_handler.py](lambda/webhook_handler.py)
- S3: [terraform/s3.tf](terraform/s3.tf)
- IAM: [terraform/iam.tf](terraform/iam.tf)

**Meta:**
- Setup: [docs/META_SETUP.md](docs/META_SETUP.md)
- Webhooks: [lambda/webhook_handler.py](lambda/webhook_handler.py) linha 50-100

**IA/Gemini:**
- Configuração: [docs/GEMINI_SETUP.md](docs/GEMINI_SETUP.md)
- Código: [lambda/webhook_handler.py](lambda/webhook_handler.py) linha 150-230
- Treinamento: [docs/AI_TRAINING.md](docs/AI_TRAINING.md)

**Segurança:**
- IAM: [terraform/iam.tf](terraform/iam.tf)
- Validação: [lambda/webhook_handler.py](lambda/webhook_handler.py) linha 80-95
- Credenciais: `ACESSOS-PRIVADO.md`

**Custos:**
- Análise: [docs/CUSTOS.md](docs/CUSTOS.md)
- Otimização: [docs/CUSTOS.md](docs/CUSTOS.md) seção Otimizações

---

## 📋 CHECKLISTS

### Antes do Deploy
Ver [PROXIMOS-PASSOS.md](PROXIMOS-PASSOS.md) - Seção Checklist

### Após Deploy
Ver [PROXIMOS-PASSOS.md](PROXIMOS-PASSOS.md) - Seção Pós-Deploy

### Segurança
Ver `ACESSOS-PRIVADO.md` - Seção Checklist de Segurança

---

## 🎯 COMANDOS ÚTEIS

### Deploy
```bash
cd terraform && ./deploy.sh
```

### Logs
```bash
aws logs tail /aws/lambda/chat-admc-webhook-handler --follow
```

### Custos
```bash
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

### Destruir
```bash
cd terraform && ./destroy.sh
```

### Teste Local
```bash
python test_local.py
```

---

## 📞 SUPORTE

### Documentação
- Todos os guias estão na pasta raiz e em `docs/`
- Cada arquivo tem seção de troubleshooting

### Recursos Externos
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Meta Developers](https://developers.facebook.com/docs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

## 🗺️ MAPA DO PROJETO

```
chat-admc/
│
├── 📄 ESTE ARQUIVO (INDEX.md)
├── 📄 README.md              → Comece aqui
├── 📄 RESUMO.md              → Visão geral técnica
├── 📄 QUICKSTART.md          → Deploy rápido
├── 📄 PROXIMOS-PASSOS.md     → Guia passo a passo
├── 📄 ACESSOS-PRIVADO.md     → Credenciais (NÃO commitado)
│
├── 📁 lambda/                → Código Python
│   ├── webhook_handler.py   → Handler principal
│   └── requirements.txt     → Dependências
│
├── 📁 terraform/             → Infraestrutura
│   ├── *.tf                 → Recursos AWS
│   ├── *.sh                 → Scripts automação
│   └── tfvars.example       → Template config
│
└── 📁 docs/                  → Documentação detalhada
    ├── META_SETUP.md        → Config Meta
    ├── AI_TRAINING.md       → Treinar IA
    ├── CUSTOS.md            → Análise custos
    ├── *.drawio             → Diagramas
    └── *.txt                → Templates
```

---

## ⏱️ TIMELINE ESTIMADA

| Fase | Tempo | Documentação |
|------|-------|--------------|
| Leitura inicial | 15 min | [README.md](README.md) |
| Setup Meta | 10 min | [docs/META_SETUP.md](docs/META_SETUP.md) |
| Deploy AWS | 10 min | [QUICKSTART.md](QUICKSTART.md) |
| Config Webhooks | 5 min | [docs/META_SETUP.md](docs/META_SETUP.md) |
| Testes | 5 min | [PROXIMOS-PASSOS.md](PROXIMOS-PASSOS.md) |
| Personalização | 30 min | [docs/AI_TRAINING.md](docs/AI_TRAINING.md) |
| **TOTAL** | **1h15min** | - |

---

## 🎓 NÍVEIS DE CONHECIMENTO

### Iniciante
Comece por:
1. [README.md](README.md)
2. [PROXIMOS-PASSOS.md](PROXIMOS-PASSOS.md)
3. [QUICKSTART.md](QUICKSTART.md)

### Intermediário
Você vai precisar de:
1. [docs/META_SETUP.md](docs/META_SETUP.md)
2. [docs/AI_TRAINING.md](docs/AI_TRAINING.md)
3. [terraform/](terraform/)

### Avançado
Explore:
1. [lambda/webhook_handler.py](lambda/webhook_handler.py)
2. [terraform/*.tf](terraform/)
3. [docs/CUSTOS.md](docs/CUSTOS.md)

---

**Última atualização:** 30/12/2024  
**Versão do projeto:** 1.0  
**Total de arquivos:** 25
