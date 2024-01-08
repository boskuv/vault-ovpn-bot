from datetime import datetime
from contextlib import suppress
from typing import Any, Optional
from jinja2 import Template
import json
import os
import hvac
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.types import FSInputFile
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

    manager.dialog_data["chosen_vpn_server"] = selected_item

    await manager.switch_to(OvpnDialogSG.set_tunnel_option)


async def on_tunnel_option_set(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    selected_item: str,
):
    # await callback.answer(bool(selected_item)) # TODO: fix

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
    await manager.switch_to(OvpnDialogSG.choose_interface)


async def on_interface_chosen(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    selected_item: str,
):
    await callback.answer(selected_item)

    manager.dialog_data["chosen_interface"] = selected_item.lower()
    await manager.switch_to(OvpnDialogSG.summarize)


async def on_confirmation(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
):
    is_able_to_generate_cert = True

    chat_id = callback.message.chat.id
    bot = callback.bot
    message_id = callback.message.message_id

    if not os.path.exists(
        manager.dialog_data["kwargs"]["config"].path_to_ovpn_template
    ):
        with suppress(TelegramBadRequest):
            is_able_to_generate_cert = False
            await bot.send_message(
                chat_id, "Шаблон ovpn-конфигурации отсутствует во входном каталоге"
            )

    client = hvac.Client(manager.dialog_data["kwargs"]["config"].vault.address)

    if os.path.exists("%s/.vault-token" % os.path.expanduser("~")):
        with open("%s/.vault-token" % os.path.expanduser("~"), "r") as f:
            client.token = f.readline().replace("\n", "")
    else:
        with suppress(TelegramBadRequest):
            is_able_to_generate_cert = False
            await bot.send_message(chat_id, "Токен отсутствует во входном каталоге")

    try:
        assert client.is_authenticated()
    except:
        is_able_to_generate_cert = False
        await bot.send_message(
            chat_id,
            "Не удалось получить доступ к инстансу vault. Обратитесь к администраторам",  # TODO: logging
        )

    if client.seal_status["sealed"]:
        is_able_to_generate_cert = False
        await bot.send_message(chat_id, "Инстанс vault запечатан")  # TODO: logging

    if is_able_to_generate_cert:
        # TODO: if manager.event.from_user.first_name is null
        cn = f"{manager.dialog_data['chosen_vpn_server']}-{manager.event.from_user.first_name}-{manager.event.from_user.id}"

        # Get list of certificates to check if common name already exists and .. TODO
        # for cert_serial in client.list(
        #     "%s/certs"% manager.dialog_data["kwargs"]["config"].vault.pki_mountpoint
        # )["data"]["keys"]:
        #     record = client.read(
        #         "%s/cert/%s"
        #         % (
        #             manager.dialog_data["kwargs"]["config"].vault.pki_mountpoint,
        #             cert_serial,
        #         )
        #     )
        #     cert = x509.load_pem_x509_certificate(
        #         record["data"]["certificate"].encode(), default_backend()
        #     )
        #     cn_ = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        #     current_datetime = datetime.now()
        #     expiration_datetime = cert.not_valid_after
        #     if cn == cn_ and current_datetime < expiration_datetime:
        #         pass
        #         # if it is possible to renew
        #         break

        # TODO: try

        result = client.write(
            f'{manager.dialog_data["kwargs"]["config"].vault.pki_mountpoint}/issue/{manager.dialog_data["kwargs"]["config"].vault.role}',
            common_name=cn,
            ttl=f"{manager.dialog_data['kwargs']['config'].vault.ttl}",
        )

        index_of_chosen_vpn_server = -1
        index_of_chosen_interface = -1

        for index, vpn_server in enumerate(
            manager.dialog_data["kwargs"]["config"].vpn_servers
        ):
            if vpn_server.name == manager.dialog_data["chosen_vpn_server"]:
                index_of_chosen_vpn_server = index
                break

        for index, interface in enumerate(
            manager.dialog_data["kwargs"]["config"]
            .vpn_servers[index_of_chosen_vpn_server]
            .interfaces
        ):
            if interface.interface_type == manager.dialog_data["chosen_interface"]:
                index_of_chosen_interface = index
                break

        if index_of_chosen_interface == -1 or index_of_chosen_vpn_server == -1:
            await bot.send_message(
                chat_id,
                f"Не удалось получить информацию о выбранном сервере: {vpn_server.name == manager.dialog_data['chosen_vpn_server']}. Обратитесь к администратору",
            )
        else:
            with open(
                manager.dialog_data["kwargs"]["config"].path_to_ovpn_template
            ) as f:
                vars = {
                    "remote_host": manager.dialog_data["kwargs"]["config"]
                    .vpn_servers[index_of_chosen_vpn_server]
                    .host,
                    "remote_port": manager.dialog_data["kwargs"]["config"]
                    .vpn_servers[index_of_chosen_vpn_server]
                    .interfaces[index_of_chosen_interface]
                    .port,
                    "tunnel_option": manager.dialog_data["tunnel_option"],
                    "push_dns_server_option": manager.dialog_data[
                        "push_dns_server_option"
                    ],
                    "chosen_interface": manager.dialog_data["chosen_interface"],
                    "routes": manager.dialog_data["kwargs"]["config"]
                    .vpn_servers[index_of_chosen_vpn_server]
                    .routes,
                    "key": result["data"]["private_key"],
                    "cert": result["data"]["certificate"],
                    "dns_server_address": manager.dialog_data["kwargs"][
                        "config"
                    ].dns.address,
                    "dns_server_domain": manager.dialog_data["kwargs"][
                        "config"
                    ].dns.domain,
                }
                rendered_template = Template(f.read()).render(vars)

                output_file_name = f"./temp/{manager.dialog_data['chosen_interface']}_{cn}_{datetime.now().strftime('%Y-%m-%d')}.ovpn"
                manager.dialog_data["output_file_name"] = output_file_name
                with open(output_file_name, "w") as file:
                    file.write(rendered_template)

            await bot.send_document(
                chat_id=chat_id,
                caption=f"Сертификат, используемый в конфигурационном файле, будет действителен в течение {manager.dialog_data['kwargs']['config'].vault.ttl}",
                document=FSInputFile(
                    path=manager.dialog_data["output_file_name"],
                    filename=manager.dialog_data["output_file_name"],
                ),
                allow_sending_without_reply=False,
                reply_to_message_id=message_id,
            )  # TODO: delete output_file_name

            await bot.send_message(
                manager.dialog_data["kwargs"]["config"].logs_chat_id,
                f"Пользователь {manager.event.from_user.first_name} (ID: {manager.event.from_user.id}) сгенерировал сертификат с CN `{cn}` для доступа к серверу `{manager.dialog_data['chosen_vpn_server']}` сроком на {manager.dialog_data['kwargs']['config'].vault.ttl}",
            )


async def on_finish(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs
):
    message_id = c.message.message_id
    chat_id = c.message.chat.id

    bot = dialog_manager.middleware_data["bot"]

    with suppress(TelegramBadRequest):
        await bot.delete_message(chat_id=chat_id, message_id=message_id)


__all__ = [
    "on_server_chosen",
    "on_tunnel_option_set",
    "on_push_dns_server_option_set",
    "on_interface_chosen",
    "on_confirmation",
]
