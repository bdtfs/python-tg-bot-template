from telegram import (
    Bot,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MessageEntity,
)
from telegram import (
    Message as TelegramMessage,
)

from app.model import Message


class TelegramClient:
    async def send(self, message: TelegramMessage, reply: Message) -> None:
        await message.reply_text(
            reply.text,
            entities=self._entities(reply),
            reply_markup=self._markup(reply),
        )

    async def acknowledge(self, query: CallbackQuery, text: str = "") -> None:
        await query.answer(text)

    async def send_to_chat(self, bot: Bot, chat_id: int, reply: Message) -> None:
        await bot.send_message(
            chat_id=chat_id,
            text=reply.text,
            entities=self._entities(reply),
            reply_markup=self._markup(reply),
        )

    async def edit(self, query: CallbackQuery, reply: Message) -> None:
        await query.edit_message_text(
            text=reply.text,
            entities=self._entities(reply),
            reply_markup=self._markup(reply),
        )

    @classmethod
    def _entities(cls, reply: Message) -> tuple[MessageEntity, ...] | None:
        entities = tuple(
            MessageEntity(
                type=MessageEntity.BOLD,
                offset=cls._utf16_length(reply.text[: span.start]),
                length=cls._utf16_length(reply.text[span.start : span.start + span.length]),
            )
            for span in reply.emphasis
        )
        return entities or None

    @staticmethod
    def _markup(reply: Message) -> InlineKeyboardMarkup | None:
        if not reply.buttons:
            return None
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        button.label,
                        callback_data=f"cmd_{button.action.value}",
                    )
                    for button in row
                ]
                for row in reply.buttons
            ]
        )

    @staticmethod
    def _utf16_length(value: str) -> int:
        return len(value.encode("utf-16-le")) // 2
