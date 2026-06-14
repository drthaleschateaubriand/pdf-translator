#!/bin/bash
# Wrapper para Mac/Linux
# Uso: ./traduzir.sh arquivo.pdf [opcoes]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Ativar venv se existir
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

# Carregar .env se existir
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^' "$SCRIPT_DIR/.env" | xargs)
fi

python3 "$SCRIPT_DIR/translate.py" "$@"
