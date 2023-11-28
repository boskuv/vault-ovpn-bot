from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class ChatMemberMiddleware(BaseMiddleware):
    def __init__(self, members_chat_id: int) -> None:
        self.members_chat_id = members_chat_id

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        
        chat_member = await event.bot.get_chat_member(self.members_chat_id, event.from_user.id)
        if chat_member.status not in ("left", "kicked"):
            return await handler(event, data)


__all__ = ["ChatMemberMiddleware"]
