from app.model import Emphasis
from app.usecases.help import HelpUseCase


def test_help_preserves_visible_copy_and_bold_heading() -> None:
    reply = HelpUseCase().execute()

    assert reply.text == (
        "Available commands:\n\n"
        "/start - Welcome message\n/help - This help text\n/ping - Health check"
    )
    assert reply.emphasis == (Emphasis(start=0, length=len("Available commands:")),)
