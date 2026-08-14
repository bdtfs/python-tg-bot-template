from app.model import Message
from app.usecases.ping import PingUseCase


def test_ping_preserves_pong_reply() -> None:
    assert PingUseCase().execute() == Message("pong")
