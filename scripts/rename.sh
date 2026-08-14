#!/usr/bin/env bash
set -euo pipefail

# Rename the template to a new bot name.
# Usage: ./scripts/rename.sh my-new-bot

NEW_NAME="${1:?Usage: ./scripts/rename.sh <new-bot-name>}"
OLD_NAME="python-tg-bot"

echo "Renaming template from '$OLD_NAME' to '$NEW_NAME'..."

# Update Makefile docker image name.
sed -i '' "s|${OLD_NAME}|${NEW_NAME}|g" Makefile 2>/dev/null || \
sed -i "s|${OLD_NAME}|${NEW_NAME}|g" Makefile

echo "Done. Bot renamed to '$NEW_NAME'."
echo "Don't forget to update CLAUDE.md if needed."
