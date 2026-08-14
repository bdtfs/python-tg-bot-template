from app.model import Message


class PingUseCase:
    def execute(self) -> Message:
        return Message("pong")
