from app.model import Message


class CancelActionUseCase:
    def execute(self) -> Message:
        return Message("Cancelled.")
