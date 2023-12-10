from contextlib import suppress
from typing import Any, Optional
import json

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.bot.states import OvpnDialogSG


async def on_server_chosen(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    selected_item: str,
):
    await callback.answer(selected_item)

    manager.dialog_data["chosen_vpn_server"] = {
        key: value.strip("'")
        for key, value in (item.split("=") for item in selected_item.split())
    }

    await manager.switch_to(OvpnDialogSG.set_tunnel_option)


async def on_tunnel_option_set(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    selected_item: str,
):
    # await callback.answer(bool(selected_item))

    manager.dialog_data["tunnel_option"] = json.loads(selected_item.lower())

    await manager.switch_to(OvpnDialogSG.push_dns_server)


async def on_push_dns_server_option_set(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    selected_item: str,
):
    await callback.answer(selected_item)

    manager.dialog_data["push_dns_server_option"] = json.loads(selected_item.lower())
    await manager.switch_to(OvpnDialogSG.summarize)


async def on_confirmation(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
):
    pass
    # await manager.switch_to(OvpnDialogSG.render_ovpn_file)


async def on_finish(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs
):
    message_id = c.message.message_id
    chat_id = c.message.chat.id

    bot = dialog_manager.middleware_data["bot"]

    with suppress(TelegramBadRequest):
        await bot.delete_message(chat_id=chat_id, message_id=message_id)


#     Реакция на нажатие кнопки выбора категории
#     """
#     msg = obj.message
#     bot = dialog_manager.middleware_data["bot"]
#     chat_id = msg.chat.id
#     context = dialog_manager.current_context()
#     search_type = selected_text.strip()

#     # завершить диалог подготовки поиска
#     await bot.delete_message(
#         chat_id=chat_id, message_id=dialog_manager.current_stack().last_message_id
#     )

#     # получить стартовые данные из контекста
#     search_phrase = context.start_data["search_phrase"]
#     search_requirements_kwargs = context.start_data["search_requirements_kwargs"]
#     initial_message = context.start_data["initial_message"]

#     asyncio.create_task(
#         run_search_tasks(
#             category=IdentifierCategory(search_type),
#             message=initial_message,
#             search_phrase=search_phrase,
#             **search_requirements_kwargs,
#         )
#     )
#     await dialog_manager.done()


# async def on_finish(
#     c: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs
# ):
#     message_id = c.message.message_id
#     chat_id = c.message.chat.id
#     await finish(
#         message_id=message_id,
#         chat_id=chat_id,
#         dialog_manager=dialog_manager,
#     )


__all__ = [
    "on_server_chosen",
    "on_tunnel_option_set",
    "on_push_dns_server_option_set",
    "on_confirmation",
]
