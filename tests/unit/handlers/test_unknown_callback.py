import pytest

from app.handlers.unknown_callback import build_handler
from tests.unit.handlers._fakes import FakeClient, callback_update, context


@pytest.mark.asyncio
async def test_unknown_callback_is_acknowledged_without_a_message() -> None:
    client = FakeClient()
    update = callback_update("unknown")

    await build_handler(client)(update, context())

    assert client.acknowledged == [(update.callback_query, "")]
    assert client.sent_to_chat == []
    assert client.edited == []
