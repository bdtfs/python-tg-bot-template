from telegram import Update
from telegram.ext import ContextTypes

from app.handlers._ports import Handler, MessagePort
from app.usecases.echo import EchoUseCase


def build_handler(use_case: EchoUseCase, client: MessagePort) -> Handler:
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if update.effective_message is None:
            return
        await client.send(
            update.effective_message,
            use_case.execute(update.effective_message.text or ""),
        )

    return handle
