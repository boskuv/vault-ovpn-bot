# from contextlib import suppress
# from typing import Optional

# from aiogram.exceptions import TelegramBadRequest
# from aiogram.types import Message
# from aiogram_dialog import DialogManager
# from sulguk import SULGUK_PARSE_MODE

# from src.enums import Emoji


# async def finish(
#     message_id: int,
#     chat_id: int,
#     dialog_manager: DialogManager,
# ) -> None:
#     """
#     Функция завершения диалога
#     :param message_id:
#     :param chat_id:
#     :param dialog_manager:
#     :return:
#     """

#     bot = dialog_manager.middleware_data["bot"]
#     initial_message: Optional[Message] = dialog_manager.start_data.get(
#         "initial_message", None
#     )
#     if isinstance(initial_message, Message):
#         initial_message_id = initial_message.message_id
#     else:
#         initial_message_id = None

#     with suppress(TelegramBadRequest):
#         await bot.delete_message(chat_id=chat_id, message_id=message_id)

#     await bot.send_message(
#         chat_id=chat_id,
#         text=f"""
#         Спасибо! {Emoji.OK}
#         <br/>
#         <br/>
#         {Emoji.WARNING} Для старта нового поиска отправь идентификатор.""",
#         reply_to_message_id=initial_message_id,
#         parse_mode=SULGUK_PARSE_MODE,
#     )


# __all__ = ["finish"]
