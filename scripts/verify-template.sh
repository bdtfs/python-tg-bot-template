#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

mkdir "$TEMP_DIR/template"
cp -R \
    "$ROOT_DIR/.dockerignore" \
    "$ROOT_DIR/.env.example" \
    "$ROOT_DIR/.gitignore" \
    "$ROOT_DIR/.python-version" \
    "$ROOT_DIR/AGENTS.md" \
    "$ROOT_DIR/CLAUDE.md" \
    "$ROOT_DIR/Dockerfile" \
    "$ROOT_DIR/Makefile" \
    "$ROOT_DIR/README.md" \
    "$ROOT_DIR/__main__.py" \
    "$ROOT_DIR/app" \
    "$ROOT_DIR/architecture.toml" \
    "$ROOT_DIR/pyproject.toml" \
    "$ROOT_DIR/requirements.lock" \
    "$ROOT_DIR/scripts" \
    "$ROOT_DIR/tests" \
    "$ROOT_DIR/uv.lock" \
    "$TEMP_DIR/template/"

if "$TEMP_DIR/template/scripts/rename.sh" "Bad Name" >/dev/null 2>&1; then
    echo "rename accepted an invalid service name" >&2
    exit 1
fi

"$TEMP_DIR/template/scripts/rename.sh" "sample-bot" >/dev/null
cd "$TEMP_DIR/template"
grep -Fq 'name = "sample-bot"' pyproject.toml
grep -Fq 'DOCKER_IMAGE ?= sample-bot:develop' Makefile
cmp AGENTS.md CLAUDE.md
uv lock --check
PYTHONDONTWRITEBYTECODE=1 uv run --frozen python -c 'import app.container, app.runtime'
