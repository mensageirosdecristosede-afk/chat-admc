#!/bin/bash

# Script de deploy completo da infraestrutura

set -e

echo "🚀 Deploy do Chat ADMC"
echo "======================="
echo ""

# Verificar se o terraform.tfvars existe
if [ ! -f "terraform.tfvars" ]; then
    echo "❌ Erro: arquivo terraform.tfvars não encontrado!"
    echo "📝 Copie o arquivo terraform.tfvars.example e preencha com suas informações:"
    echo "   cp terraform.tfvars.example terraform.tfvars"
    exit 1
fi

# Verificar se as credenciais AWS estão configuradas
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ Erro: Credenciais AWS não configuradas!"
    echo "📝 Configure suas credenciais AWS:"
    echo "   export AWS_ACCESS_KEY_ID=sua_access_key"
    echo "   export AWS_SECRET_ACCESS_KEY=sua_secret_key"
    exit 1
fi

echo "✅ Credenciais AWS verificadas"
echo "👤 Account: $(aws sts get-caller-identity --query Account --output text)"
echo ""

# Criar Lambda Layer
echo "📦 Criando Lambda Layer..."
./create_layer.sh
echo ""

# Terraform init
echo "🔧 Inicializando Terraform..."
terraform init
echo ""

# Terraform plan
echo "📋 Planejando mudanças..."
terraform plan -out=tfplan
echo ""

# Confirmar deploy
read -p "🤔 Deseja aplicar as mudanças? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "❌ Deploy cancelado"
    exit 0
fi

# Terraform apply
echo "🚀 Aplicando infraestrutura..."
terraform apply tfplan
echo ""

# Remover plano
rm -f tfplan

echo ""
echo "✅ Deploy concluído com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure o webhook no Meta Developer Console"
echo "2. Faça upload do contexto da igreja para o S3"
echo "3. Teste o webhook"
echo ""
echo "📖 Veja o README.md para instruções detalhadas"
