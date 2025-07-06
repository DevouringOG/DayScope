from typing import List
from aiogram import Router

from .start import start_router
from .tasks import title_handler, value_handler


__all__ = ["title_handler", "value_handler"]


def get_routers() -> List[Router]:
    return (
        start_router,
    )
