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

import elastic_agent_client.generated.elastic_agent_client_pb2 as proto

AGENT_PROTOCOL_TO_PYTHON_LOG_LEVEL = {
    proto.UnitLogLevel.ERROR: logging.ERROR,
    proto.UnitLogLevel.WARN: logging.WARNING,
    proto.UnitLogLevel.INFO: logging.INFO,
    proto.UnitLogLevel.DEBUG: logging.DEBUG,
    proto.UnitLogLevel.TRACE: logging.DEBUG,
}


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


def convert_agent_log_level(agent_log_level):
    """
    Maps a log level from the protobuf UnitLogLevel enum to a Python
    logging level.

    Since the UnitLogLevel enum doesn't directly map to Python's logging integer levels,
    this function provides a manual mapping to convert between the two.

    If an unknown log level is provided, the function defaults to logging.INFO.
    """

    return AGENT_PROTOCOL_TO_PYTHON_LOG_LEVEL.get(agent_log_level, logging.INFO)


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
