from pydantic import SecretStr

from app.config import Settings


def test_token_is_not_exposed_by_settings_representation() -> None:
    settings = Settings(
        telegram_bot_token=SecretStr("123:ABC"),
        _env_file=None,
    )

    assert "123:ABC" not in repr(settings)
    assert settings.telegram_bot_token.get_secret_value() == "123:ABC"
