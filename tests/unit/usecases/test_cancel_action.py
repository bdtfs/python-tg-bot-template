from app.model import Message
from app.usecases.cancel_action import CancelActionUseCase


def test_cancellation_preserves_existing_copy() -> None:
    assert CancelActionUseCase().execute() == Message("Cancelled.")
