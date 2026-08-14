import pytest

from app.handlers.start import build_handler
from app.usecases.start import StartUseCase
from tests.unit.handlers._fakes import FakeClient, context, message_update


@pytest.mark.asyncio
async def test_start_maps_user_and_message_before_sending() -> None:
    client = FakeClient()
    update = message_update()

    await build_handler(StartUseCase(), client)(update, context())

    assert client.sent[0][0] is update.effective_message
    assert client.sent[0][1].text.startswith("Hello, Ada!")
