from typing import Any, cast

from pydantic import SecretStr
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler

from app.config import Settings
from app.container import build


def test_container_registers_each_operation_in_precedence_order() -> None:
    container = build(Settings(telegram_bot_token=SecretStr("123:ABC"), _env_file=None))

    handlers = container.application.handlers[0]

    assert [type(handler) for handler in handlers] == [
        CommandHandler,
        CommandHandler,
        CommandHandler,
        CallbackQueryHandler,
        CallbackQueryHandler,
        CallbackQueryHandler,
        CallbackQueryHandler,
        MessageHandler,
    ]
    command_handlers = [cast(CommandHandler[Any, Any], handler) for handler in handlers[:3]]
    assert [handler.commands for handler in command_handlers] == [
        frozenset({"start"}),
        frozenset({"help"}),
        frozenset({"ping"}),
    ]
    assert container.log_level == "INFO"
