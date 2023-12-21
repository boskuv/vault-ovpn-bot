from typing import Dict, List, Optional, Literal

# from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    """
    Bot config
    """

    token: SecretStr


class VpnConfig(BaseSettings):
    """
    VPN config
    """

    name: str
    host: str
    port: int  # TODO: >0
    ttl: str


class VaultConfig(BaseSettings):
    address: str
    pki_mountpoint: str
    role: str


class Config(BaseSettings):
    """
    All in one config
    """

    bot: BotConfig
    vault: VaultConfig
    chat_id: int
    logs_chat_id: int
    vpn_servers: List[VpnConfig] = dict()


__all__ = ["BotConfig", "Config"]
