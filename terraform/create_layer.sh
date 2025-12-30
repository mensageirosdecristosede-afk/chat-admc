#!/bin/bash

# Script para criar Lambda Layer com dependências Python

set -e

echo "🔨 Criando Lambda Layer para Chat ADMC..."

# Diretório do layer
LAYER_DIR="lambda_layer/python"
ZIP_FILE="lambda_layer.zip"

# Limpar diretório anterior
rm -rf lambda_layer
rm -f "$ZIP_FILE"

# Criar estrutura de diretórios
mkdir -p "$LAYER_DIR"

# Instalar dependências no diretório do layer
echo "📦 Instalando dependências..."
pip install -r ../lambda/requirements.txt -t "$LAYER_DIR" --upgrade

# Criar ZIP do layer
echo "📦 Criando arquivo ZIP..."
cd lambda_layer
zip -r "../$ZIP_FILE" . -q
cd ..

# Limpar diretório temporário
rm -rf lambda_layer

echo "✅ Lambda Layer criado: $ZIP_FILE"
echo "📊 Tamanho: $(du -h $ZIP_FILE | cut -f1)"
