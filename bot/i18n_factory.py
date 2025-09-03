from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

DIR_PATH = Path("locales")


def get_translator_hub() -> TranslatorHub:
    """
    Create and return a TranslatorHub configured with available locales.
    """
    en_file = DIR_PATH / "en" / "LC_MESSAGES" / "txt.ftl"
    ru_file = DIR_PATH / "ru" / "LC_MESSAGES" / "txt.ftl"

    return TranslatorHub(
        locales_map={"en": ("en", "ru"), "ru": ("ru", "en")},
        translators=[
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en",
                    filenames=[str(en_file)],
                ),
            ),
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru",
                    filenames=[str(ru_file)],
                ),
            ),
        ],
    )
