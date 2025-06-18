import structlog
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handling.states import StartSG
from database.requests import add_user


start_router = Router()


@start_router.message(CommandStart())
async def start(msg: Message, dialog_manager: DialogManager, session: AsyncSession):
    await add_user(
        session=session,
        telegram_id=msg.from_user.id,
        lang=msg.from_user.language_code,
    )
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
