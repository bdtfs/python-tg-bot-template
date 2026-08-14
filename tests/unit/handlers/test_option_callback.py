import pytest

from app.handlers.option_callback import build_handler
from app.usecases.select_option import SelectOptionUseCase
from tests.unit.handlers._fakes import FakeClient, callback_update, context


@pytest.mark.asyncio
async def test_option_callback_acknowledges_and_sends_to_the_callback_chat() -> None:
    client = FakeClient()
    update = callback_update("cmd_option_a")
    callback_context = context()

    await build_handler(SelectOptionUseCase(), client)(update, callback_context)

    assert client.acknowledged == [(update.callback_query, "Loading...")]
    assert client.sent_to_chat[0][0] is callback_context.bot
    assert client.sent_to_chat[0][1] == 42
    assert client.sent_to_chat[0][2].text == "You picked Option A."


@pytest.mark.asyncio
async def test_option_callback_falls_back_to_the_user_chat() -> None:
    client = FakeClient()

    await build_handler(SelectOptionUseCase(), client)(
        callback_update("cmd_option_b", with_message=False), context()
    )

    assert client.sent_to_chat[0][1] == 7
