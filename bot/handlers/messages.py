from telegram import Update
from telegram.ext import ContextTypes

from bot.clients.telegram import TelegramClient
from bot.handlers.types import Handler
from bot.usecases.reply import ReplyUseCase


def build_handler(use_case: ReplyUseCase, client: TelegramClient) -> Handler:
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        text = update.effective_message.text if update.effective_message else ""
        await client.send(update, use_case.echo(text or ""))

    return handle
