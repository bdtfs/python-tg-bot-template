#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOCK_COPY="$(mktemp)"
trap 'rm -f "$LOCK_COPY"' EXIT

cd "$ROOT_DIR"
uv lock --check
uv export --frozen --no-header --no-dev --no-emit-project --format requirements-txt -o "$LOCK_COPY" >/dev/null
cmp requirements.lock "$LOCK_COPY"
