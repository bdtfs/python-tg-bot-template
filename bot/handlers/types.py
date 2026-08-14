from collections.abc import Callable, Coroutine
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

Handler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, None]]
