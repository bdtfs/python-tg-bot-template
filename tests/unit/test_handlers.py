from types import SimpleNamespace
from typing import Any

import pytest

from bot.handlers import callbacks, help, messages, ping, start
from bot.model import CallbackReply, Reply
from bot.usecases.reply import ReplyUseCase


class FakeClient:
    def __init__(self) -> None:
        self.reply: Reply | None = None
        self.callback_reply: CallbackReply | None = None

    async def send(self, update: Any, reply: Reply) -> None:
        self.reply = reply

    async def callback(self, update: Any, context: Any, reply: CallbackReply) -> None:
        self.callback_reply = reply


@pytest.mark.asyncio
class TestHandlers:
    async def test_start(self) -> None:
        client = FakeClient()
        update = SimpleNamespace(effective_user=SimpleNamespace(first_name="Ada"))
        await start.build_handler(ReplyUseCase(), client)(update, None)  # type: ignore[arg-type]
        assert client.reply is not None and "Ada" in client.reply.text

    async def test_help(self) -> None:
        client = FakeClient()
        await help.build_handler(ReplyUseCase(), client)(SimpleNamespace(), None)  # type: ignore[arg-type]
        assert client.reply is not None and "/start" in client.reply.text

    async def test_ping(self) -> None:
        client = FakeClient()
        await ping.build_handler(ReplyUseCase(), client)(SimpleNamespace(), None)  # type: ignore[arg-type]
        assert client.reply == Reply("pong")

    async def test_message(self) -> None:
        client = FakeClient()
        update = SimpleNamespace(effective_message=SimpleNamespace(text="hello"))
        await messages.build_handler(ReplyUseCase(), client)(update, None)  # type: ignore[arg-type]
        assert client.reply == Reply("You said: hello")

    async def test_callback(self) -> None:
        client = FakeClient()
        update = SimpleNamespace(
            callback_query=SimpleNamespace(data="confirm_delete"),
            effective_user=SimpleNamespace(id=1),
        )
        await callbacks.build_handler(ReplyUseCase(), client)(update, None)  # type: ignore[arg-type]
        assert client.callback_reply is not None and client.callback_reply.edit
