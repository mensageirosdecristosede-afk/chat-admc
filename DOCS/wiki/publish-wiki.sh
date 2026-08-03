#!/bin/bash
# Publica os docs de DOCS/wiki/ na wiki do GitHub
# Pré-requisito: inicializar a wiki pelo web UI (criar pelo menos uma página)
# depois rodar este script

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIKI_SRC="$REPO_DIR/DOCS/wiki"
WIKI_REMOTE="git@github-chat-admc:mensageirosdecristosede-afk/chat-admc.wiki.git"
WIKI_TMP="/tmp/chat-admc-wiki-deploy"

echo "==> Clonando wiki..."
rm -rf "$WIKI_TMP"
git clone "$WIKI_REMOTE" "$WIKI_TMP"

echo "==> Copiando páginas..."
cp "$WIKI_SRC"/*.md "$WIKI_TMP/"

echo "==> Commitando..."
cd "$WIKI_TMP"
git add -A
git commit -m "docs(wiki): publicar documentação v1.0.0" || echo "Nada a commitar"

echo "==> Publicando..."
git push origin master

echo "==> Wiki publicada com sucesso!"
echo "    https://github.com/mensageirosdecristosede-afk/chat-admc/wiki"
