from app.model import Message


class ConfirmActionUseCase:
    def execute(self, action: str) -> Message:
        return Message(f"Confirmed: {action}")
