import json
from typing import Any

import pytest
from telegram import Bot
from telegram.request import BaseRequest, RequestData

from app.clients.telegram import TelegramClient
from app.model import Action, Button, Emphasis, Message


class RecordingRequest(BaseRequest):
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def initialize(self) -> None:
        return None

    async def shutdown(self) -> None:
        return None

    @property
    def read_timeout(self) -> float | None:
        return None

    async def do_request(
        self,
        url: str,
        method: str,
        request_data: RequestData | None = None,
        read_timeout: Any = None,
        write_timeout: Any = None,
        connect_timeout: Any = None,
        pool_timeout: Any = None,
    ) -> tuple[int, bytes]:
        del method, read_timeout, write_timeout, connect_timeout, pool_timeout
        operation = url.rsplit("/", maxsplit=1)[-1]
        parameters = dict(request_data.parameters) if request_data else {}
        self.calls.append((operation, parameters))
        if operation == "getMe":
            result: Any = {
                "id": 1,
                "is_bot": True,
                "first_name": "Template",
                "username": "template_bot",
            }
        elif operation == "sendMessage":
            result = {
                "message_id": 1,
                "date": 0,
                "chat": {"id": parameters["chat_id"], "type": "private"},
                "text": parameters["text"],
            }
        else:
            result = True
        return 200, json.dumps({"ok": True, "result": result}).encode()


@pytest.mark.asyncio
async def test_adapter_uses_the_real_bot_api_serialization_boundary() -> None:
    request = RecordingRequest()
    bot = Bot(token="123:ABC", request=request)
    reply = Message(
        text="Choose Option A",
        emphasis=(Emphasis(start=7, length=8),),
        buttons=((Button("Option A", Action.OPTION_A),),),
    )

    async with bot:
        await TelegramClient().send_to_chat(bot, 42, reply)

    operation, parameters = request.calls[-1]
    assert operation == "sendMessage"
    assert parameters["chat_id"] == 42
    assert parameters["text"] == "Choose Option A"
    assert parameters["entities"] == [{"length": 8, "offset": 7, "type": "bold"}]
    assert parameters["reply_markup"] == {
        "inline_keyboard": [[{"callback_data": "cmd_option_a", "text": "Option A"}]]
    }
