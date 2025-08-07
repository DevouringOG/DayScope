from aiogram_dialog.widgets.text import Text
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition 
from fluentogram import TranslatorRunner
from fluent_compiler.errors import FluentReferenceError
from fluentogram.exceptions import FormatError
import structlog


logger = structlog.get_logger(__name__)


class I18NFormat(Text):
    def __init__(self, key: str, when: WhenCondition = None):
        self.key = key
        super().__init__(when)

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        i18n: TranslatorRunner = manager.middleware_data.get("i18n")
        try:
            text = i18n.get(self.key, **data)
        except (FluentReferenceError, FormatError):
            text = i18n.get(self.key, **manager.dialog_data)
        if text is None:
            raise KeyError(f'translation key = "{self.key}" not found')
        return text
