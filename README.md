# Projeto: chat-admc

Resumo: este repositório contém o código e a infraestrutura para o chatbot/integrações do projeto "Igreja ADMC". O objetivo é manter código, scripts de deploy e documentação para ambientes AWS e GCP de forma organizada e auditável.

**Estrutura do repositório**

- `docs/`: documentação, contexto do projeto, guias e arquivos de referência (treinamento de AI, arquitetura, custos, etc.).
- `ENV-AWS/`: artefatos e infraestrutura para implantação no AWS. Contém:
  - `aws-terraform/`: configurações Terraform, scripts de deploy e pacotes (lambda, layer) usados para deploy na AWS.
  - `lambda/`: código-fonte (webhook handler) e dependências para a função Lambda.
  - arquivos auxiliares e exemplos de uso/variáveis.
- `gcp-terraform/`: infraestrutura e artefatos para implantação no Google Cloud (Cloud Functions, storage, Terraform para GCP).

Outros itens importantes:
- `test_local.py`: script auxiliar para testes locais.

**Objetivo de cada pasta**

- `docs/`: centralizar contexto da igreja, decisões arquiteturais, instruções operacionais e histórico.
- `ENV-AWS/aws-terraform/`: declarar, construir e publicar recursos AWS (API Gateway, Lambda, IAM, S3, etc.).
- `ENV-AWS/lambda/`: manter o código da função Lambda preparado para empacotamento e deploy (requirements e handler).
- `gcp-terraform/`: alternativa para executar a mesma lógica em GCP (Cloud Function + Storage), com scripts de deploy e arquivos Terraform.

**Como o projeto está sendo pensado**

- Separação clara entre documentação, código da função e infraestrutura como código (IaC). Isso facilita revisão, auditoria e deploy independente por provedor.
- Ambientes são mantidos dentro de pastas (`ENV-AWS`, `gcp-terraform`) para evitar misturar configurações específicas de cada provedor.
- Segredos não devem estar em commits — use variáveis de ambiente, secrets managers (Secrets Manager, Secret Manager do GCP) ou arquivos ignorados (`.gitignore`).

**Deploy (visão geral)**

- AWS (resumo):
  1. Preparar credenciais seguras e variáveis (não commitar).
 2. Entrar em `ENV-AWS/aws-terraform/`, ajustar `terraform.tfvars`, executar `terraform init` e `terraform apply`.
 3. Empacotar `/ENV-AWS/lambda/` se necessário e subir artefatos para S3 (scripts de `deploy.sh` já presentes).

- GCP (resumo):
  1. Configurar `gcloud` e permissões.
 2. Entrar em `gcp-terraform/`, ajustar `terraform.tfvars`, executar `terraform init` e `terraform apply`.
 3. Usar `deploy_function.sh` para subir o código da Cloud Function, se necessário.

**Observações de segurança e housekeeping**

- Rotacione imediatamente qualquer chave que tenha vazado em commits anteriores. Este repositório teve commits contendo chaves; o histórico foi reescrito localmente para remover alguns arquivos, mas credenciais devem ser consideradas comprometidas.
- Nunca adicione credenciais em texto puro no repositório. Use `.gitignore` e variáveis/secret managers.

**Próximos passos recomendados**

- Validar e atualizar os `README` específicos dentro de `ENV-AWS` e `gcp-terraform` com passos detalhados de deploy.
- Adicionar CI/CD (GitHub Actions) para lint, testes e verificação de secrets antes do push.
- Documentar processo de rotação de credenciais e adição de novos colaboradores.

Se quiser, eu atualizo este `README.md` com instruções mais detalhadas de deploy (com comandos) ou adiciono READMEs por pasta.
