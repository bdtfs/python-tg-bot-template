from dataclasses import dataclass

from telegram.ext import Application, ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from bot.clients.telegram import TelegramClient
from bot.config import Settings
from bot.handlers import callbacks, help, messages, ping, start
from bot.usecases.reply import ReplyUseCase


@dataclass(frozen=True)
class Container:
    application: Application


def build(settings: Settings) -> Container:
    application = ApplicationBuilder().token(settings.telegram_bot_token).build()
    use_case = ReplyUseCase()
    client = TelegramClient()

    application.add_handler(CommandHandler("start", start.build_handler(use_case, client)))
    application.add_handler(CommandHandler("help", help.build_handler(use_case, client)))
    application.add_handler(CommandHandler("ping", ping.build_handler(use_case, client)))
    application.add_handler(CallbackQueryHandler(callbacks.build_handler(use_case, client)))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages.build_handler(use_case, client)))
    return Container(application)
