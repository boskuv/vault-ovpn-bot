from aiogram_dialog import Dialog
from aiogram_dialog import LaunchMode

from .windows import (
    choose_vpn_server_window,
    set_tunnel_option_window,
    push_dns_server_option_window,
    summarize_window,
)


ovpn_dialog = Dialog(
    choose_vpn_server_window(),
    set_tunnel_option_window(),
    push_dns_server_option_window(),
    summarize_window(),
    launch_mode=LaunchMode.ROOT,
)


__all__ = ["search_dialog"]
