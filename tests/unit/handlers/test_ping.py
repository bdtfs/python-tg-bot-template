import pytest

from app.handlers.ping import build_handler
from app.model import Message
from app.usecases.ping import PingUseCase
from tests.unit.handlers._fakes import FakeClient, context, message_update


@pytest.mark.asyncio
async def test_ping_sends_pong() -> None:
    client = FakeClient()

    await build_handler(PingUseCase(), client)(message_update(), context())

    assert client.sent[0][1] == Message("pong")
