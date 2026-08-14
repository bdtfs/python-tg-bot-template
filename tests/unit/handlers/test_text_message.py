import pytest

from app.handlers.text_message import build_handler
from app.model import Message
from app.usecases.echo import EchoUseCase
from tests.unit.handlers._fakes import FakeClient, context, message_update


@pytest.mark.asyncio
async def test_text_message_maps_text_to_echo() -> None:
    client = FakeClient()

    await build_handler(EchoUseCase(), client)(message_update("hello"), context())

    assert client.sent[0][1] == Message("You said: hello")
