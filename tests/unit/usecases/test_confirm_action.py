from app.model import Message
from app.usecases.confirm_action import ConfirmActionUseCase


def test_confirmation_preserves_existing_copy() -> None:
    assert ConfirmActionUseCase().execute("delete") == Message("Confirmed: delete")
