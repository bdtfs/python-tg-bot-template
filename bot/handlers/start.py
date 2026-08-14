from telegram import Update
from telegram.ext import ContextTypes

from bot.clients.telegram import TelegramClient
from bot.handlers.types import Handler
from bot.usecases.reply import ReplyUseCase


def build_handler(use_case: ReplyUseCase, client: TelegramClient) -> Handler:
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if update.effective_user is None:
            return
        await client.send(update, use_case.start(update.effective_user.first_name))

    return handle
