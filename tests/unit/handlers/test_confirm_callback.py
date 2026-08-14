import pytest

from app.handlers.confirm_callback import build_handler
from app.model import Message
from app.usecases.confirm_action import ConfirmActionUseCase
from tests.unit.handlers._fakes import FakeClient, callback_update, context


@pytest.mark.asyncio
async def test_confirm_callback_acknowledges_and_replaces_the_message() -> None:
    client = FakeClient()
    update = callback_update("confirm_delete")

    await build_handler(ConfirmActionUseCase(), client)(update, context())

    assert client.acknowledged == [(update.callback_query, "Confirmed: delete")]
    assert client.edited == [(update.callback_query, Message("Confirmed: delete"))]
