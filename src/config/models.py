from typing import Dict, List, Optional, Literal

# from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    """
    Bot config
    """

    token: SecretStr


class Interface(BaseSettings):
    interface_type: Literal["tun", "tap"] = "tun"
    port: int


class VpnConfig(BaseSettings):
    """
    VPN config
    """

    name: str
    host: str
    interfaces: list[Interface]  # TODO: if more than one tun/tap
    routes: list = list()


class VaultConfig(BaseSettings):
    address: str
    pki_mountpoint: str
    role: str
    ttl: str


class Config(BaseSettings):
    """
    All in one config
    """

    bot: BotConfig
    vault: VaultConfig
    team_chat_id: int
    logs_chat_id: int
    vpn_servers: List[VpnConfig] = dict()


__all__ = ["BotConfig", "Config"]
