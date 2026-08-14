from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.model import CallbackReply, Reply


class TelegramClient:
    async def send(self, update: Update, reply: Reply) -> None:
        if update.effective_message is None:
            return
        markup = None
        if reply.buttons:
            markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(button.text, callback_data=button.data) for button in row] for row in reply.buttons]
            )
        await update.effective_message.reply_text(
            reply.text,
            parse_mode=reply.parse_mode,
            reply_markup=markup,
        )

    async def callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        reply: CallbackReply,
    ) -> None:
        query = update.callback_query
        if query is None:
            return
        await query.answer(reply.acknowledgement)
        if not reply.message:
            return
        if reply.edit:
            await query.edit_message_text(reply.message)
            return
        chat_id = query.message.chat_id if query.message else update.effective_user.id
        await context.bot.send_message(chat_id=chat_id, text=reply.message, parse_mode="HTML")
