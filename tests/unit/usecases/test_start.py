from app.model import Action
from app.usecases.start import StartUseCase


def test_start_builds_the_existing_personalized_menu() -> None:
    reply = StartUseCase().execute("Ada")

    assert reply.text == "Hello, Ada!\n\nI'm your bot. Use /help or pick an option."
    assert [button.label for button in reply.buttons[0]] == ["Option A", "Option B"]
    assert [button.action for button in reply.buttons[0]] == [Action.OPTION_A, Action.OPTION_B]
