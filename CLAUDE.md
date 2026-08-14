# Python Telegram bot template

This template follows `../../../agent-docs/SERVICE-STRUCTURE.md`.

```text
bot/
├── __main__.py                 thin module entrypoint
├── config.py                   validated settings, no import-time singleton
├── container.py                application composition and handler registration
├── model.py                    transport-independent values
├── handlers/<operation>.py     one operation per module
├── usecases/<domain>.py        application behavior
└── clients/telegram.py         Telegram output adapter
tests/unit/                     use-case, handler, and architecture suites
```

Handlers map `Update` values, call a use case, and send through the injected Telegram
client. Use cases never import `telegram`, handlers, settings, or the container. The
container is the only place that constructs concrete dependencies and registers routes.

```bash
python -m pip install -r requirements-dev.txt
make test
make lint
make run
```

`TELEGRAM_BOT_TOKEN` is required. Add a new operation as one handler module plus tests,
then register its injected factory in `container.py`. Comments explain constraints only.
