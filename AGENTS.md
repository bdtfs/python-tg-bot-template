# Python Telegram bot template

This repository is the canonical Python Telegram bot service template. Its boundaries are a
release gate.

```text
__main__.py                     lifecycle-only entrypoint
app/config.py                   validated environment settings
app/container.py                sole concrete composition root
app/model.py                    transport-independent values
app/handlers/<operation>.py     one Telegram operation per module
app/handlers/_ports.py          narrow transport ports
app/usecases/<behavior>.py      pure application behavior
app/clients/telegram.py         Telegram presentation adapter
tests/architecture/             blocking dependency and ownership rules
tests/unit/                     behavior and mapping tests
tests/integration/              framework and adapter boundary tests
```

Handlers extract Telegram values, invoke one use case, and send through an injected port. Use
cases import only application values. They contain no Telegram, HTML, parse-mode, callback
acknowledgement, or message-edit semantics. Clients never import handlers or use cases. Only the
container constructs concrete dependencies.

The template has no persistence behavior, so `app/storage` is intentionally absent. Do not add
empty or in-memory production storage. A real persistence requirement must add a use-case-owned
port, a concrete adapter, integration coverage, and set `architecture.toml` accordingly.

```bash
uv sync --frozen
make check
make docker-build
make run
```

`TELEGRAM_BOT_TOKEN` is required to run. Add an operation as one handler module, one pure use case
where behavior exists, owning tests, and one container registration. Comments explain constraints
only. `CLAUDE.md` and `AGENTS.md` must remain byte-identical.
