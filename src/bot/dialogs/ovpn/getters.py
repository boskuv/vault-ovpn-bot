from aiogram_dialog import DialogManager


async def init_data_getter(dialog_manager: DialogManager, **kwargs):
    for k, v in dialog_manager.start_data.items():
        dialog_manager.dialog_data[k] = v

    dialog_manager.start_data["vpn_servers"] = [
        server_cfg.name for server_cfg in dialog_manager.start_data["vpn_servers"]
    ]
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


async def tuntap_inteface_getter(dialog_manager: DialogManager, **kwargs):
    tuntap_intefaces = list()

    for vpn_server_cfg in kwargs["config"].vpn_servers:
        if vpn_server_cfg.name == dialog_manager.dialog_data["chosen_vpn_server"]:
            for (
                interface
            ) in vpn_server_cfg.interfaces:  # TODO: compulsory params and more than 2
                tuntap_intefaces.append(
                    (interface.interface_type.lower(), interface.interface_type.lower())
                )
    return {
        "tuntap_intefaces": tuntap_intefaces,
        "count": len(tuntap_intefaces),
    }


async def summarize_getter(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.dialog_data

    return {
        "chosen_vpn_server": dialog_data["chosen_vpn_server"],
        "push_dns_server_option": dialog_data["push_dns_server_option"],
        "tunnel_option": dialog_data["tunnel_option"],
        "chosen_interface": dialog_data["chosen_interface"],
        "period": kwargs["config"].vault.ttl,
    }


__all__ = [
    "init_data_getter",
    "true_false_option_getter",
    "tuntap_inteface_getter",
    "summarize_getter",
    "render_ovpn_file_getter",
]
