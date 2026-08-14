import logging

from bot.config import Settings
from bot.container import build


def main() -> None:
    settings = Settings()  # type: ignore[call-arg]
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    build(settings).application.run_polling(drop_pending_updates=False)
