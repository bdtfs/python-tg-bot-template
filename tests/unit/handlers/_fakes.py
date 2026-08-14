from types import SimpleNamespace
from typing import Any

from app.model import Message


class FakeClient:
    def __init__(self) -> None:
        self.sent: list[tuple[Any, Message]] = []
        self.acknowledged: list[tuple[Any, str]] = []
        self.sent_to_chat: list[tuple[Any, int, Message]] = []
        self.edited: list[tuple[Any, Message]] = []

    async def send(self, message: Any, reply: Message) -> None:
        self.sent.append((message, reply))

    async def acknowledge(self, query: Any, text: str = "") -> None:
        self.acknowledged.append((query, text))

    async def send_to_chat(self, bot: Any, chat_id: int, reply: Message) -> None:
        self.sent_to_chat.append((bot, chat_id, reply))

    async def edit(self, query: Any, reply: Message) -> None:
        self.edited.append((query, reply))


def context() -> Any:
    return SimpleNamespace(bot=object())


def message_update(text: str = "") -> Any:
    return SimpleNamespace(
        effective_user=SimpleNamespace(first_name="Ada", id=7),
        effective_message=SimpleNamespace(text=text),
        callback_query=None,
    )


def callback_update(data: str, *, with_message: bool = True) -> Any:
    query_message = SimpleNamespace(chat=SimpleNamespace(id=42)) if with_message else None
    return SimpleNamespace(
        effective_user=SimpleNamespace(first_name="Ada", id=7),
        effective_message=query_message,
        callback_query=SimpleNamespace(data=data, message=query_message),
    )
