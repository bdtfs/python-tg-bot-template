# python-tg-bot-template

Canonical async Telegram bot service skeleton with explicit composition, operation handlers, pure
use cases, an isolated Telegram adapter, deterministic dependencies, and blocking architecture
tests.

```bash
cp .env.example .env
uv sync --frozen
make check
make run
```

Create a named service from the template with `./scripts/rename.sh my-bot`. See `CLAUDE.md` for the
mandatory boundaries and extension rules.
