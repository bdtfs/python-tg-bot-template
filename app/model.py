from dataclasses import dataclass
from enum import StrEnum


class Action(StrEnum):
    OPTION_A = "option_a"
    OPTION_B = "option_b"


@dataclass(frozen=True, slots=True)
class Button:
    label: str
    action: Action


@dataclass(frozen=True, slots=True)
class Emphasis:
    start: int
    length: int


@dataclass(frozen=True, slots=True)
class Message:
    text: str
    emphasis: tuple[Emphasis, ...] = ()
    buttons: tuple[tuple[Button, ...], ...] = ()
