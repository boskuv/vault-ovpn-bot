from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.memory import SimpleEventIsolation
from structlog.stdlib import BoundLogger

from src.config import Config
from src.bot.dialogs import register_dialogs
from src.bot.handlers import register_handlers
from src.bot.middlewares import LoggerMiddleware, ChatMemberMiddleware


def setup_dispatcher(
    logger: BoundLogger, config: Config, team_chat_id: int
) -> Dispatcher:
    """
    :param logger:
    :param chat_id:
    :return:
    """
    dp: Dispatcher = Dispatcher(
        storage=MemoryStorage(),
        config=config,
        logger=logger,
        team_chat_id=team_chat_id,
        events_isolation=SimpleEventIsolation(),
    )
    dp.message.middleware(LoggerMiddleware(logger=logger))
    dp.message.middleware(ChatMemberMiddleware(team_chat_id))

    register_dialogs(dp)
    register_handlers(dp)

    return dp


__all__ = ["setup_dispatcher"]
