from telegram import Update
from telegram.ext import ContextTypes

from bot.clients.telegram import TelegramClient
from bot.handlers.types import Handler
from bot.usecases.reply import ReplyUseCase


def build_handler(use_case: ReplyUseCase, client: TelegramClient) -> Handler:
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        await client.send(update, use_case.help())

    return handle
