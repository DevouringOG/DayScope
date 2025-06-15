from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator


DIR_PATH = "I18N/locales"


def i18n_factory() -> TranslatorHub:
    return TranslatorHub(
        locales_map={
            "en": ("en", "ru"),
            "ru": ("ru", "en"),
        },
        translators=[
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en",
                    filenames=[f"{DIR_PATH}/en/LC_MESSAGES/txt.ftl"],
                ),
            ),
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru",
                    filenames=[f"{DIR_PATH}/ru/LC_MESSAGES/txt.ftl"],
                ),
            ),
        ],
    )