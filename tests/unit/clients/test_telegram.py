from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest
from telegram import MessageEntity

from app.clients.telegram import TelegramClient
from app.model import Action, Button, Emphasis, Message


@pytest.mark.asyncio
async def test_send_maps_semantic_formatting_and_actions_to_telegram() -> None:
    telegram_message: Any = SimpleNamespace(reply_text=AsyncMock())
    reply = Message(
        "Hello Ada",
        emphasis=(Emphasis(start=6, length=3),),
        buttons=((Button("Option A", Action.OPTION_A),),),
    )

    await TelegramClient().send(telegram_message, reply)

    telegram_message.reply_text.assert_awaited_once()
    call = telegram_message.reply_text.await_args
    assert call.args == ("Hello Ada",)
    assert call.kwargs["entities"] == (MessageEntity(type=MessageEntity.BOLD, offset=6, length=3),)
    assert call.kwargs["reply_markup"].inline_keyboard[0][0].callback_data == "cmd_option_a"


def test_entity_offsets_are_converted_to_telegram_utf16_units() -> None:
    reply = Message("👋 Ada", emphasis=(Emphasis(start=2, length=3),))

    assert TelegramClient._entities(reply) == (
        MessageEntity(type=MessageEntity.BOLD, offset=3, length=3),
    )
