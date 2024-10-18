#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from google.protobuf.struct_pb2 import Struct

import elastic_agent_client.generated.elastic_agent_client_pb2 as proto
from elastic_agent_client.client import V2
from elastic_agent_client.service.actions import ActionsService
from elastic_agent_client.util.async_tools import AsyncIterator


@pytest.fixture
def action_handler():
    action_handler = Mock()
    action_handler.handle_action = AsyncMock()
    return action_handler


@pytest.fixture
def v2_client():
    v2_client = V2()
    v2_client.client = Mock()
    v2_client.client.CheckinV2 = Mock()
    v2_client.client.Actions = MagicMock()
    v2_client.sync_component = Mock()
    v2_client.sync_units = Mock()
    return v2_client


@pytest.fixture
def additional_unit():
    return proto.UnitExpected(
        id="unit-2",
        type=proto.UnitType.INPUT,
        state=proto.State.STARTING,
        config_state_idx=1,
        config=proto.UnitExpectedConfig(
            source=Struct(),
            id="config-2",
            type="unit-config",
            name="additional_unit",
            revision=None,
            meta=None,
            data_stream=None,
            streams=None,
        ),
        log_level=proto.UnitLogLevel.INFO,
    )


@pytest.mark.asyncio
async def test_run_with_no_grpc_client(v2_client, action_handler):
    v2_client.client = None
    action_service = ActionsService(v2_client, action_handler)
    with pytest.raises(RuntimeError):
        await action_service.run()


@pytest.mark.asyncio
async def test_run_sends_init_action_on_startup(v2_client, action_handler):
    v2_client.units = None
    action_service = ActionsService(v2_client, action_handler)
    with patch("asyncio.Queue.__new__", Mock()) as queue_init_mock:
        queue_mock = AsyncMock()
        queue_init_mock.return_value = queue_mock

        await action_service.run()

        queue_mock.put.assert_called_once()
        # Check that we send an init signal on startup
        assert queue_mock.put.call_args[0][0].id == "init"


@pytest.mark.asyncio
async def test_run_handles_actions_stream(v2_client, action_handler):
    queue = []
    queue.append(
        proto.ActionRequest(
            id="action-1",
            name="Something Something",
            params=b"",
            unit_id="some_unit_id",
            unit_type=proto.UnitType.INPUT,
            type=proto.ActionRequest.Type.CUSTOM,
            level=proto.ActionRequest.Level.ALL,
        )
    )
    v2_client.client.Actions = Mock(return_value=AsyncIterator(queue))

    action_service = ActionsService(v2_client, action_handler)

    await action_service.run()


@pytest.mark.asyncio
async def test_run_handles_exception_in_action_handler(v2_client, action_handler):
    # First set up the message sent
    queue = []
    queue.append(
        proto.ActionRequest(
            id="action-1",
            name="Something Something",
            params=b"",
            unit_id="some_unit_id",
            unit_type=proto.UnitType.INPUT,
            type=proto.ActionRequest.Type.CUSTOM,
            level=proto.ActionRequest.Level.ALL,
        )
    )
    v2_client.client.Actions = Mock(return_value=AsyncIterator(queue))

    # Then make action handler error out
    action_handler.handle_action.side_effect = [Exception("Whoopsie")]

    # Init service
    action_service = ActionsService(v2_client, action_handler)

    # Then run it and observe
    with patch("asyncio.Queue.__new__", Mock()) as queue_init_mock:
        queue_mock = AsyncMock()
        queue_init_mock.return_value = queue_mock

        await action_service.run()

        queue_mock.put.assert_called()
        assert queue_mock.put.call_count == 2  # 1 for init, 1 for failed message
        # Check that we send the failed signal back
        assert queue_mock.put.call_args[0][0].status == proto.ActionResponse.FAILED
        assert queue_mock.put.call_args[0][0].id == "action-1"
