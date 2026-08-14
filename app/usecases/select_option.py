from app.model import Action, Emphasis, Message


class SelectOptionUseCase:
    def execute(self, action: Action) -> Message:
        label = "Option A" if action is Action.OPTION_A else "Option B"
        return Message(
            text=f"You picked {label}.",
            emphasis=(Emphasis(start=len("You picked "), length=len(label)),),
        )
