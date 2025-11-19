from typing import Optional

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession


def get_i18n(dialog_manager: DialogManager) -> Optional[TranslatorRunner]:
    return dialog_manager.middleware_data.get("i18n")


def get_session(dialog_manager: DialogManager) -> Optional[AsyncSession]:
    return dialog_manager.middleware_data.get("session")
