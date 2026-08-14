from telegram import Update
from telegram.ext import ContextTypes

from app.handlers._ports import Handler, MessagePort
from app.usecases.ping import PingUseCase


def build_handler(use_case: PingUseCase, client: MessagePort) -> Handler:
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if update.effective_message is None:
            return
        await client.send(update.effective_message, use_case.execute())

    return handle
