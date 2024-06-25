#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
"""
Logger -- sets the logging and provides a `logger` global object.
"""
import logging
from functools import cached_property

logger: logging.Logger


class ColorFormatter(logging.Formatter):
    GREY = "\x1b[38;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    DATE_FMT = "%H:%M:%S"

    def __init__(self, prefix):
        self.custom_format = "[" + prefix + "][%(asctime)s][%(levelname)s] %(message)s"
        super().__init__()

    @cached_property
    def debug_formatter(self):
        return logging.Formatter(
            fmt=self.GREY + self.custom_format + self.RESET, datefmt=self.DATE_FMT
        )

    @cached_property
    def info_formatter(self):
        return logging.Formatter(
            fmt=self.GREEN + self.custom_format + self.RESET, datefmt=self.DATE_FMT
        )

    @cached_property
    def warning_formatter(self):
        return logging.Formatter(
            fmt=self.YELLOW + self.custom_format + self.RESET, datefmt=self.DATE_FMT
        )

    @cached_property
    def error_formatter(self):
        return logging.Formatter(
            fmt=self.RED + self.custom_format + self.RESET, datefmt=self.DATE_FMT
        )

    @cached_property
    def critical_formatter(self):
        return logging.Formatter(
            fmt=self.BOLD_RED + self.custom_format + self.RESET, datefmt=self.DATE_FMT
        )

    def format(self, record):  # noqa: A003
        formatter = getattr(self, f"{record.levelname.lower()}_formatter")
        return formatter.format(record)


class ExtraLogger(logging.Logger):
    def _log(
        self,
        level,
        msg,
        args,
        exc_info=None,
        extra=None,
        stack_info=None,
        stacklevel=None,
        prefix=None,
    ):
        if prefix:
            msg = f"{prefix} {msg}"

        if extra is None:
            extra = {}
        super(ExtraLogger, self)._log(level, msg, args, exc_info, extra)


def set_logger(log_level=logging.INFO):
    global logger
    formatter = ColorFormatter("FMWK")

    if logger is None:
        logging.setLoggerClass(ExtraLogger)
        logger = logging.getLogger("agent-client-py")
        logger.handlers.clear()
        handler = logging.StreamHandler()
        logger.addHandler(handler)

    logger.propagate = False
    logger.setLevel(log_level)
    logger.handlers[0].setLevel(log_level)
    logger.handlers[0].setFormatter(formatter)
    return logger


set_logger()
