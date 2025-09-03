import logging

import structlog

from config import LogsConfig


def startup(config: LogsConfig):
    pre_chain = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(
            fmt=config.timestamp_format, utc=False
        ),
    ]

    handler = logging.StreamHandler()
    handler.set_name("default")
    handler.setLevel(config.level)

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(colors=True),
        ],
        foreign_pre_chain=pre_chain,
    )

    handler.setFormatter(formatter)

    logging.basicConfig(handlers=(handler,), level=config.level)
    structlog.configure(
        processors=[
            *pre_chain,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
