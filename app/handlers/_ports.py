from collections.abc import Callable, Coroutine
from typing import Any, Protocol

from telegram import Bot, CallbackQuery, Update
from telegram import Message as TelegramMessage
from telegram.ext import ContextTypes

from app.model import Message

type Handler = Callable[
    [Update, ContextTypes.DEFAULT_TYPE],
    Coroutine[Any, Any, None],
]


class MessagePort(Protocol):
    async def send(self, message: TelegramMessage, reply: Message) -> None: ...


class CallbackPort(Protocol):
    async def acknowledge(self, query: CallbackQuery, text: str = "") -> None: ...

    async def send_to_chat(self, bot: Bot, chat_id: int, reply: Message) -> None: ...

    async def edit(self, query: CallbackQuery, reply: Message) -> None: ...
