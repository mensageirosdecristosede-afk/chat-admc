#!/bin/bash

# Script para destruir toda a infraestrutura

set -e

echo "⚠️  DESTRUIR INFRAESTRUTURA"
echo "==========================="
echo ""
echo "Este script irá DESTRUIR TODOS os recursos AWS criados pelo Terraform!"
echo "Isso inclui:"
echo "  - Lambda Function"
echo "  - API Gateway"
echo "  - S3 Bucket (e TODO o conteúdo)"
echo "  - IAM Roles e Policies"
echo "  - CloudWatch Logs"
echo ""

read -p "🤔 Tem certeza que deseja continuar? Digite 'DESTRUIR' para confirmar: " confirm

if [ "$confirm" != "DESTRUIR" ]; then
    echo "❌ Operação cancelada"
    exit 0
fi

echo ""
echo "🗑️  Destruindo infraestrutura..."

# Esvaziar bucket S3 primeiro (Terraform não pode deletar bucket com conteúdo)
BUCKET_NAME=$(terraform output -raw s3_bucket_name 2>/dev/null || echo "")
if [ -n "$BUCKET_NAME" ]; then
    echo "🗑️  Esvaziando bucket S3: $BUCKET_NAME"
    aws s3 rm "s3://$BUCKET_NAME" --recursive || true
fi

# Terraform destroy
terraform destroy -auto-approve

echo ""
echo "✅ Infraestrutura destruída com sucesso!"
