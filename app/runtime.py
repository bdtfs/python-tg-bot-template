import logging

from app.container import build_from_environment


def main() -> None:
    container = build_from_environment()
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=getattr(logging, container.log_level.upper(), logging.INFO),
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    container.application.run_polling(drop_pending_updates=False)
