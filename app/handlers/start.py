from telegram import Update
from telegram.ext import ContextTypes

from app.handlers._ports import Handler, MessagePort
from app.usecases.start import StartUseCase


def build_handler(use_case: StartUseCase, client: MessagePort) -> Handler:
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if update.effective_user is None or update.effective_message is None:
            return
        await client.send(
            update.effective_message,
            use_case.execute(update.effective_user.first_name),
        )

    return handle
