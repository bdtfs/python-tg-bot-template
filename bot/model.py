from dataclasses import dataclass, field


@dataclass(frozen=True)
class Button:
    text: str
    data: str


@dataclass(frozen=True)
class Reply:
    text: str
    parse_mode: str | None = None
    buttons: list[list[Button]] = field(default_factory=list)


@dataclass(frozen=True)
class CallbackReply:
    acknowledgement: str = ""
    message: str = ""
    edit: bool = False
