from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class OvpnDialogSG(StatesGroup):
    choose_vpn_server = State()
    set_tunnel_option = State()
    push_dns_server = State()
    summarize = State()
    render_ovpn_file = State()


__all__ = ["OvpnDialogSG"]
