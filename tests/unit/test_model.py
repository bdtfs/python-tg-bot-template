import pytest

from app.model import Action


def test_only_shipped_menu_actions_are_valid() -> None:
    assert Action("option_a") is Action.OPTION_A
    assert Action("option_b") is Action.OPTION_B
    with pytest.raises(ValueError):
        Action("unknown")
