from aiogram_dialog import DialogManager


async def init_data_getter(dialog_manager: DialogManager, **kwargs):
    for k, v in dialog_manager.start_data.items():
        dialog_manager.dialog_data[k] = v

    init_data = dialog_manager.start_data if dialog_manager.start_data else {}

    return init_data


async def true_false_option_getter(**kwargs):
    true_false_options = [
        ("✅", True),
        ("❌", False),
    ]
    return {
        "true_false_options": true_false_options,
        "count": len(true_false_options),
    }


async def summarize_getter(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.dialog_data

    return {
        "chosen_vpn_server": dialog_data["chosen_vpn_server"]["host"],
        "push_dns_server_option": dialog_data["push_dns_server_option"],
        "tunnel_option": dialog_data["tunnel_option"],
        "period": "1d",  # TODO
    }


__all__ = [
    "init_data_getter",
    "true_false_option_getter",
    "summarize_getter",
    "render_ovpn_file_getter",
]
