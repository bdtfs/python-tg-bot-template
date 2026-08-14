from bot.usecases.reply import ReplyUseCase


class TestReplyUseCase:
    def test_start_builds_personalized_menu(self) -> None:
        reply = ReplyUseCase().start("Ada")
        assert "Ada" in reply.text
        assert reply.buttons[0][0].data == "cmd_option_a"

    def test_confirm_callback_is_an_edit(self) -> None:
        reply = ReplyUseCase().callback("confirm_delete")
        assert reply.edit is True
        assert reply.message == "Confirmed: delete"
