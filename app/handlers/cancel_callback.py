from telegram import Update
from telegram.ext import ContextTypes

from app.handlers._ports import CallbackPort, Handler
from app.usecases.cancel_action import CancelActionUseCase


def build_handler(use_case: CancelActionUseCase, client: CallbackPort) -> Handler:
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        query = update.callback_query
        if query is None or query.data is None or update.effective_user is None:
            return
        await client.acknowledge(query, "Cancelled")
        await client.edit(query, use_case.execute())

    return handle
