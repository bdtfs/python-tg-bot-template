from app.model import Message
from app.usecases.echo import EchoUseCase


def test_echo_preserves_existing_copy() -> None:
    assert EchoUseCase().execute("hello") == Message("You said: hello")
