from app.model import Action, Button, Message


class StartUseCase:
    def execute(self, first_name: str) -> Message:
        return Message(
            text=f"Hello, {first_name}!\n\nI'm your bot. Use /help or pick an option.",
            buttons=(
                (
                    Button("Option A", Action.OPTION_A),
                    Button("Option B", Action.OPTION_B),
                ),
            ),
        )
