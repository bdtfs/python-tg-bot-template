from bot.model import Button, CallbackReply, Reply


class ReplyUseCase:
    def start(self, first_name: str) -> Reply:
        return Reply(
            text=f"Hello, {first_name}!\n\nI'm your bot. Use /help or pick an option.",
            buttons=[[Button("Option A", "cmd_option_a"), Button("Option B", "cmd_option_b")]],
        )

    def help(self) -> Reply:
        return Reply(
            text=(
                "<b>Available commands:</b>\n\n"
                "/start - Welcome message\n/help - This help text\n/ping - Health check"
            ),
            parse_mode="HTML",
        )

    def ping(self) -> Reply:
        return Reply("pong")

    def echo(self, text: str) -> Reply:
        return Reply(f"You said: {text}")

    def callback(self, data: str) -> CallbackReply:
        if data == "cmd_option_a":
            return CallbackReply("Loading...", "You picked <b>Option A</b>.")
        if data == "cmd_option_b":
            return CallbackReply("Loading...", "You picked <b>Option B</b>.")
        if data.startswith("confirm_"):
            action = data.removeprefix("confirm_")
            return CallbackReply(f"Confirmed: {action}", f"Confirmed: {action}", edit=True)
        if data.startswith("cancel_"):
            return CallbackReply("Cancelled", "Cancelled.", edit=True)
        return CallbackReply()
