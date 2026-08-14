from telegram import Update
from telegram.ext import ContextTypes

from app.handlers._ports import CallbackPort, Handler
from app.usecases.confirm_action import ConfirmActionUseCase


def build_handler(use_case: ConfirmActionUseCase, client: CallbackPort) -> Handler:
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        query = update.callback_query
        if query is None or query.data is None or update.effective_user is None:
            return
        action = query.data.removeprefix("confirm_")
        notice = f"Confirmed: {action}"
        await client.acknowledge(query, notice)
        await client.edit(query, use_case.execute(action))

    return handle
