from typing import Dict, List, Optional, Literal
#from pydantic import Field
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
    port: int # TODO: >0

class Config(BaseSettings):
    """
    All in one config
    """

    bot: BotConfig
    chat_id: int
    vault_address: str
    vpn_servers: List[VpnConfig] = dict()


__all__ = ["BotConfig", "Config"]
