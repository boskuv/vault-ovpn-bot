from aiogram import Dispatcher

# from .admins import router as admin_router
from .misc import router as misc_router
from .ovpn import router as vpn_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(misc_router)
    dp.include_router(vpn_router)
    # dp.include_router(admin_router)


__all__ = ["register_handlers"]
