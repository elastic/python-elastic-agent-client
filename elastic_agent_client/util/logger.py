#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
"""
Logger -- sets the logging and provides a `logger` global object.
"""

import logging

import ecs_logging


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
    try:
        _logger = logger
    except NameError:
        _logger = None

    if _logger is None:
        logging.setLoggerClass(ExtraLogger)
        _logger = logging.getLogger("agent-client-py")
        _logger.handlers.clear()
        handler = logging.StreamHandler()
        handler.setFormatter(ecs_logging.StdlibFormatter())
        _logger.addHandler(handler)

    _logger.propagate = False
    _logger.setLevel(log_level)
    _logger.handlers[0].setLevel(log_level)
    return _logger


global logger
logger: logging.Logger = set_logger()
