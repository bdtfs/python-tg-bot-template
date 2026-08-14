from app.model import Message


class EchoUseCase:
    def execute(self, text: str) -> Message:
        return Message(f"You said: {text}")
