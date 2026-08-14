from telegram import Update
from telegram.ext import ContextTypes

from app.handlers._ports import CallbackPort, Handler
from app.model import Action
from app.usecases.select_option import SelectOptionUseCase


def build_handler(use_case: SelectOptionUseCase, client: CallbackPort) -> Handler:
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data is None or update.effective_user is None:
            return
        try:
            action = Action(query.data.removeprefix("cmd_"))
        except ValueError:
            return

        await client.acknowledge(query, "Loading...")
        chat_id = query.message.chat.id if query.message else update.effective_user.id
        await client.send_to_chat(context.bot, chat_id, use_case.execute(action))

    return handle
