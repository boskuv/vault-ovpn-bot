import structlog
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = structlog.stdlib.get_logger()
router = Router(name="misc")


@router.message(
    Command("start", "help"),
)  # type: ignore
async def start_help_handler(message: Message, **kwargs) -> None:
    """
    Handle /start or /help message
    :param message:
    # :param messages:
    :param kwargs:
    :return:
    """
    await message.answer(
        "test",
        disable_web_page_preview=True,
    )


__all__ = ["router"]
