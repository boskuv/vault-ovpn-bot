from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from .ovpn import ovpn_dialog


def register_dialogs(dp: Dispatcher) -> Dispatcher:
    dp.include_router(ovpn_dialog)
    setup_dialogs(dp)
    return dp


__all__ = ["register_dialogs"]
