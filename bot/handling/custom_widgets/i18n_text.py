from aiogram_dialog.widgets.text import Text
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition 
from fluentogram import TranslatorRunner


class I18NFormat(Text):
    def __init__(self, key: str, when: WhenCondition = None):
        self.key = key
        super().__init__(when)

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        i18n: TranslatorRunner = manager.middleware_data.get("i18n")
        text = i18n.get(self.key, **data)
        if text is None:
            raise KeyError(f'translation key = "{self.key}" not found')
        return text
