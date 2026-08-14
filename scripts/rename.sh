#!/usr/bin/env bash
set -euo pipefail

NEW_NAME="${1:?Usage: ./scripts/rename.sh <new-bot-name>}"
OLD_NAME="python-tg-bot-template"

if [[ ! "$NEW_NAME" =~ ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ ]]; then
    echo "Name must be kebab-case and start with a letter." >&2
    exit 1
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FILES=(
    "$ROOT_DIR/AGENTS.md"
    "$ROOT_DIR/CLAUDE.md"
    "$ROOT_DIR/Makefile"
    "$ROOT_DIR/README.md"
    "$ROOT_DIR/pyproject.toml"
    "$ROOT_DIR/requirements.lock"
    "$ROOT_DIR/uv.lock"
)

sed -i.bak "s|${OLD_NAME}|${NEW_NAME}|g" "${FILES[@]}"
for file in "${FILES[@]}"; do
    rm -f "$file.bak"
done

echo "Renamed template to '$NEW_NAME'."
