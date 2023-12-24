from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class OvpnDialogSG(StatesGroup):
    choose_vpn_server = State()
    set_tunnel_option = State()
    push_dns_server = State()
    choose_interface = State()
    summarize = State()


__all__ = ["OvpnDialogSG"]
