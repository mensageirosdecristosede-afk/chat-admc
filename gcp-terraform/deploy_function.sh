#!/bin/bash
# Script para atualizar e redeployar Cloud Function no GCP

set -e

echo "Empacotando arquivos..."
zip -r function-source.zip main.py requirements.txt church-context-gemini.txt

echo "Rodando terraform apply..."
terraform apply --auto-approve

echo "Deploy concluído!"
