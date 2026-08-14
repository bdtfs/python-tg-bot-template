# Python Telegram bot template

An async `python-telegram-bot` skeleton with explicit DI, operation-scoped handlers,
transport-independent use cases, an isolated Telegram client, and architecture tests.

```bash
cp .env.example .env
python -m pip install -r requirements-dev.txt
make test
make run
```

See `CLAUDE.md` for the mandatory folder and dependency contract.
