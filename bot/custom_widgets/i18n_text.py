from typing import Dict, Optional

import structlog
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from fluent_compiler.errors import FluentReferenceError
from fluentogram import TranslatorRunner
from fluentogram.exceptions import FormatError

from bot.utils import get_i18n

logger = structlog.get_logger(__name__)


class I18nFormat(Text):
    """
    Widget that resolves a translation key
    using fluentogram's TranslatorRunner.

    The widget will try to format with the provided rendering `data` first and
    fall back to the dialog manager's `dialog_data` on formatting/reference
    errors.
    """

    def __init__(self, key: str, when: WhenCondition = None) -> None:
        self.key = key
        super().__init__(when)

    async def _render_text(
        self,
        data: Dict[str, object],
        manager: DialogManager,
    ) -> str:
        i18n: Optional[TranslatorRunner] = get_i18n(manager)
        if i18n is None:
            logger.warning(
                "i18n translator is missing",
                key=self.key,
            )
        try:
            text = i18n.get(self.key, **data)
        except (FluentReferenceError, FormatError) as exc:
            logger.debug(
                "Formatting failed with rendering data, "
                "falling back to dialog_data",
                exc=exc,
            )
            text = i18n.get(self.key, **manager.dialog_data)

        if text is None:
            raise KeyError(f"translation key = '{self.key}' not found")
        return text
