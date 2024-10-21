#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
import asyncio
from unittest.mock import Mock

import pytest
from google.protobuf.struct_pb2 import Struct

import elastic_agent_client.generated.elastic_agent_client_pb2 as proto
from elastic_agent_client.client import V2
from elastic_agent_client.util.async_tools import AsyncQueueIterator


@pytest.fixture
def v2_client():
    v2_client = V2()
    v2_client.client = Mock()
    v2_client.client.CheckinV2 = Mock(return_value=AsyncQueueIterator(asyncio.Queue()))
    return v2_client


@pytest.fixture
def checkin_expected():
    return proto.CheckinExpected(
        units=[
            proto.UnitExpected(
                id="unit-1",
                type=proto.UnitType.INPUT,
                state=proto.State.STARTING,
                config_state_idx=1,
                config=proto.UnitExpectedConfig(
                    source=Struct(),
                    id="config-1",
                    type="test-config",
                    name="test-config-name",
                    revision=None,
                    meta=None,
                    data_stream=None,
                    streams=None,
                ),
                log_level=proto.UnitLogLevel.INFO,
            )
        ],
        agent_info=proto.AgentInfo(
            id="agent-id-1",
            version="0.1",
            snapshot=False,
            mode=proto.AgentManagedMode.STANDALONE,
        ),
        features=proto.Features(source=Struct(), fqdn=proto.FQDNFeature(enabled=False)),
        features_idx=1,
        component=proto.Component(
            limits=proto.ComponentLimits(source=Struct(), go_max_procs=0),
            apm_config=proto.APMConfig(
                elastic=proto.ElasticAPM(
                    tls=proto.ElasticAPMTLS(
                        skip_verify=False,
                        server_cert="apm_server_cert",
                        server_ca="apm_server_ca",
                    ),
                    environment="test",
                    api_key="apm_api_key",
                    secret_token="apm_secret_token",
                    hosts=["acme.com/apm-host"],
                    global_labels="apm-label",
                )
            ),
        ),
        component_idx=1,
        units_timestamp=None,
    )


@pytest.mark.asyncio
async def test_sync_units_updates_units_from_incoming_checkin_expected(
    v2_client, checkin_expected
):
    v2_client.sync_units(checkin_expected)
