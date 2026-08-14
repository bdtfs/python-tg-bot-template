import pytest

from app.handlers.help import build_handler
from app.usecases.help import HelpUseCase
from tests.unit.handlers._fakes import FakeClient, context, message_update


@pytest.mark.asyncio
async def test_help_sends_the_use_case_result() -> None:
    client = FakeClient()
    update = message_update()

    await build_handler(HelpUseCase(), client)(update, context())

    assert client.sent[0][0] is update.effective_message
    assert "/start" in client.sent[0][1].text
