from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.kbd import Group
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.kbd import Column
from aiogram_dialog.widgets.kbd import Radio
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.text import Multi
from aiogram_dialog.widgets.media import StaticMedia

import operator

from ...states import OvpnDialogSG
from .getters import init_data_getter, true_false_option_getter, summarize_getter
from .on_clicks import (
    on_server_chosen,
    on_tunnel_option_set,
    on_push_dns_server_option_set,
    on_confirmation,
    on_finish,
)


def choose_vpn_server_window() -> Window:
    return Window(
        Const("Выберите VPN-сервер, к которому хотите подключиться:"),
        Column(
            Select(
                text=Format("{item.name}"),
                id="choose_vpn",
                items="vpn_servers",
                item_id_getter=lambda x: x,
                on_click=on_server_chosen,
            )
        ),
        Group(
            Cancel(text=Const(f"⛔ Отмена"), id="cancel", on_click=on_finish),
        ),
        state=OvpnDialogSG.choose_vpn_server,
        getter=init_data_getter,
    )


def set_tunnel_option_window() -> Window:
    return Window(
        Const("Туннелировать ли трафик:"),
        Radio(
            Format("🔘 {item[0]}"),
            Format("⚪️ {item[0]}"),
            id="set_tunnel_option",
            item_id_getter=operator.itemgetter(1),
            items="true_false_options",
            on_click=on_tunnel_option_set,
        ),
        Group(
            # Back(text=Const(f"{Emoji.BACK} Назад"), id="back"),
            Cancel(text=Const(f"⛔ Отмена"), id="cancel", on_click=on_finish),
        ),
        state=OvpnDialogSG.set_tunnel_option,
        getter=true_false_option_getter,
    )


def push_dns_server_option_window() -> Window:
    return Window(
        Const("Подменять ли DNS-сервер:"),
        Radio(
            Format("🔘 {item[0]}"),
            Format("⚪️ {item[0]}"),
            id="push_dns_server_option",
            item_id_getter=operator.itemgetter(1),
            items="true_false_options",
            on_click=on_push_dns_server_option_set,
        ),
        Group(
            # Back(text=Const(f"{Emoji.BACK} Назад"), id="back"),
            Cancel(text=Const(f"⛔ Отмена"), id="cancel", on_click=on_finish),
        ),
        state=OvpnDialogSG.push_dns_server,
        getter=true_false_option_getter,
    )


def summarize_window() -> Window:
    return Window(
        Format(
            "Вы хотите сгенерировать ovpn-файл сроком на {period} со следующими параметрами:"
        ),
        Format("📃 Точка подключения: {chosen_vpn_server}"),
        Format("📃 Туннелирование трафика: {push_dns_server_option}"),
        Format("📃 Подмена dns: {tunnel_option}"),
        Group(
            Cancel(
                text=Const(f"✅ Все верно - сгенерировать!"),
                id="yes",
                on_click=on_confirmation,
            ),
            # Back(text=Const(f"{Emoji.BACK} Назад"), id="back"),
            Cancel(text=Const(f"⛔ Отмена"), id="cancel", on_click=on_finish),
        ),
        state=OvpnDialogSG.summarize,
        getter=summarize_getter,
    )


def render_ovpn_file_window() -> Window:
    return Window(
        StaticMedia(
            path="/home/tishka17/python_logo.png",
            type=ContentType.DOCUMENT,
        ),
        state=OvpnDialogSG.render_ovpn_file,
    )


__all__ = [
    "choose_vpn_server_window",
    "set_tunnel_option_window",
    "push_dns_server_option_window",
    "summarize_window",
    "render_ovpn_file_window",
]
