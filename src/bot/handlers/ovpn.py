import structlog
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode, ShowMode

from ..states import OvpnDialogSG

logger = structlog.stdlib.get_logger()
router = Router(name="vpn")


@router.message(
    Command("generate_ovpn"),
)  # type: ignore
async def generate_ovpn_handler(
    message: Message, dialog_manager: DialogManager, **kwargs
) -> None:
    """
    ...
    :param message:
    :param dialog_manager:
    :param kwargs:
    :return:
    """
    await dialog_manager.start(
        OvpnDialogSG.choose_vpn_server,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.AUTO,
        data={
            "vpn_servers": kwargs["config"].vpn_servers,
            "initial_message": message,
            "kwargs": kwargs,
        },
    )


__all__ = ["router"]
