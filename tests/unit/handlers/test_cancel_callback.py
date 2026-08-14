import pytest

from app.handlers.cancel_callback import build_handler
from app.model import Message
from app.usecases.cancel_action import CancelActionUseCase
from tests.unit.handlers._fakes import FakeClient, callback_update, context


@pytest.mark.asyncio
async def test_cancel_callback_acknowledges_and_replaces_the_message() -> None:
    client = FakeClient()
    update = callback_update("cancel_delete")

    await build_handler(CancelActionUseCase(), client)(update, context())

    assert client.acknowledged == [(update.callback_query, "Cancelled")]
    assert client.edited == [(update.callback_query, Message("Cancelled."))]
