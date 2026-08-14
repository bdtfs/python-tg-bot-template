from app.model import Emphasis, Message


class HelpUseCase:
    def execute(self) -> Message:
        heading = "Available commands:"
        return Message(
            text=(
                f"{heading}\n\n"
                "/start - Welcome message\n/help - This help text\n/ping - Health check"
            ),
            emphasis=(Emphasis(start=0, length=len(heading)),),
        )
