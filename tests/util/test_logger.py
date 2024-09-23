#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
import logging

import pytest

import elastic_agent_client.generated.elastic_agent_client_pb2 as proto
from elastic_agent_client.util.logger import convert_agent_log_level


@pytest.mark.parametrize(
    "agent_log_level, expected_log_level",
    [
        (proto.UnitLogLevel.ERROR, logging.ERROR),
        (proto.UnitLogLevel.WARN, logging.WARNING),
        (proto.UnitLogLevel.INFO, logging.INFO),
        (proto.UnitLogLevel.DEBUG, logging.DEBUG),
        (proto.UnitLogLevel.TRACE, logging.DEBUG),
        (999, logging.INFO),
    ],
)
def test_convert_agent_log_level(agent_log_level, expected_log_level):
    assert convert_agent_log_level(agent_log_level) == expected_log_level


@pytest.mark.parametrize(
    "agent_log_level, expected_log_level",
    [
        (0, logging.ERROR),
        (1, logging.WARNING),
        (2, logging.INFO),
        (3, logging.DEBUG),
        (4, logging.DEBUG),
        (42, logging.INFO),
    ],
)
def test_convert_agent_integer_log_level(agent_log_level, expected_log_level):
    assert convert_agent_log_level(agent_log_level) == expected_log_level
