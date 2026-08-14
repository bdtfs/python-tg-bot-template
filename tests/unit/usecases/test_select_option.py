from app.model import Action, Emphasis
from app.usecases.select_option import SelectOptionUseCase


def test_each_existing_option_has_the_same_visible_reply() -> None:
    use_case = SelectOptionUseCase()

    option_a = use_case.execute(Action.OPTION_A)
    option_b = use_case.execute(Action.OPTION_B)

    assert option_a.text == "You picked Option A."
    assert option_a.emphasis == (Emphasis(start=11, length=len("Option A")),)
    assert option_b.text == "You picked Option B."
    assert option_b.emphasis == (Emphasis(start=11, length=len("Option B")),)
