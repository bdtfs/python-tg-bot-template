from dataclasses import dataclass
from typing import Any

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from app.clients.telegram import TelegramClient
from app.config import Settings
from app.handlers import (
    cancel_callback,
    confirm_callback,
    help,
    option_callback,
    ping,
    start,
    text_message,
    unknown_callback,
)
from app.usecases.cancel_action import CancelActionUseCase
from app.usecases.confirm_action import ConfirmActionUseCase
from app.usecases.echo import EchoUseCase
from app.usecases.help import HelpUseCase
from app.usecases.ping import PingUseCase
from app.usecases.select_option import SelectOptionUseCase
from app.usecases.start import StartUseCase


@dataclass(frozen=True, slots=True)
class Container:
    application: Application[Any, Any, Any, Any, Any, Any]
    log_level: str


def build(settings: Settings) -> Container:
    application = ApplicationBuilder().token(settings.telegram_bot_token.get_secret_value()).build()
    client = TelegramClient()
    start_use_case = StartUseCase()
    help_use_case = HelpUseCase()
    ping_use_case = PingUseCase()
    echo_use_case = EchoUseCase()
    select_option_use_case = SelectOptionUseCase()
    confirm_action_use_case = ConfirmActionUseCase()
    cancel_action_use_case = CancelActionUseCase()

    application.add_handler(CommandHandler("start", start.build_handler(start_use_case, client)))
    application.add_handler(CommandHandler("help", help.build_handler(help_use_case, client)))
    application.add_handler(CommandHandler("ping", ping.build_handler(ping_use_case, client)))
    application.add_handler(
        CallbackQueryHandler(
            option_callback.build_handler(select_option_use_case, client),
            pattern=r"^cmd_option_(?:a|b)$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            confirm_callback.build_handler(confirm_action_use_case, client),
            pattern=r"^confirm_.*$",
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            cancel_callback.build_handler(cancel_action_use_case, client),
            pattern=r"^cancel_.*$",
        )
    )
    application.add_handler(CallbackQueryHandler(unknown_callback.build_handler(client)))
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_message.build_handler(echo_use_case, client),
        )
    )
    return Container(application=application, log_level=settings.log_level)


def build_from_environment() -> Container:
    return build(Settings())
