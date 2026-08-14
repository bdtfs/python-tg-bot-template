from telegram import Update
from telegram.ext import ContextTypes

from bot.clients.telegram import TelegramClient
from bot.handlers.types import Handler
from bot.usecases.reply import ReplyUseCase


def build_handler(use_case: ReplyUseCase, client: TelegramClient) -> Handler:
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data is None or update.effective_user is None:
            return
        await client.callback(update, context, use_case.callback(query.data))

    return handle
