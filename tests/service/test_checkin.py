#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
import asyncio
from unittest import mock
from unittest.mock import AsyncMock, Mock, call

import pytest
from google.protobuf.struct_pb2 import Struct

import elastic_agent_client.generated.elastic_agent_client_pb2 as proto
from elastic_agent_client.client import V2, Unit, VersionInfo
from elastic_agent_client.service.checkin import CheckinV2Service
from elastic_agent_client.util.async_tools import AsyncIterator, AsyncQueueIterator


@pytest.fixture
def checkin_handler():
    checkin_handler = Mock()
    checkin_handler.apply_from_client = AsyncMock()
    return checkin_handler


@pytest.fixture
def v2_client():
    v2_client = V2()
    v2_client.client = Mock()
    v2_client.client.CheckinV2 = Mock(return_value=AsyncQueueIterator(asyncio.Queue()))
    v2_client.sync_component = Mock()
    v2_client.sync_units = Mock()
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
async def test_run_error_on_unset_stub(checkin_handler):
    client = V2()  # not using the fixture
    with pytest.raises(RuntimeError):
        checkin_service = CheckinV2Service(client, checkin_handler)
        await checkin_service.run()
    checkin_handler.apply_from_client.assert_not_called()


@pytest.mark.asyncio
async def test_do_checkin(v2_client, checkin_handler):
    v2_client.units = [Unit(unit_id="1")]
    v2_client.version_info = VersionInfo(name="Test")
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    send_queue = asyncio.Queue()
    await checkin_service.do_checkin(send_queue)
    assert not send_queue.empty()
    sent = await send_queue.get()
    assert isinstance(sent, proto.CheckinObserved)
    assert len(sent.units) == 1
    assert sent.units[0].id == "1"
    assert sent.version_info.name == "Test"


@pytest.mark.asyncio
async def test_do_checkin_with_no_units(v2_client, checkin_handler):
    v2_client.units = None
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    send_queue = asyncio.Queue()
    await checkin_service.do_checkin(send_queue)
    assert send_queue.empty()


@pytest.mark.asyncio
async def test_do_checkin_when_versioninfo_sent(v2_client, checkin_handler):
    v2_client.units = [Unit()]
    v2_client.version_info_sent = True
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    send_queue = asyncio.Queue()
    await checkin_service.do_checkin(send_queue)
    assert not send_queue.empty()
    sent: proto.CheckinObserved = await send_queue.get()
    assert not sent.HasField("version_info")


@pytest.mark.asyncio
async def test_apply_expected_on_empty(v2_client, checkin_handler, checkin_expected):
    # v2_client fixture is empty
    assert v2_client.units is None
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    await checkin_service.apply_expected(checkin_expected)
    v2_client.sync_component.assert_called_once()
    v2_client.sync_units.assert_called_once()
    checkin_handler.apply_from_client.assert_awaited_once()


@pytest.mark.asyncio
async def test_apply_expected_on_changed_component(
    v2_client, checkin_handler, checkin_expected
):
    v2_client.component_idx = checkin_expected.component_idx - 1  # different component
    v2_client.units = [
        Unit(
            unit_id=checkin_expected.units[0].id,
            config_idx=checkin_expected.units[0].config_state_idx,
        )
    ]  # same units
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    await checkin_service.apply_expected(checkin_expected)

    # syncup happens
    v2_client.sync_component.assert_called_once()
    v2_client.sync_units.assert_called_once()
    checkin_handler.apply_from_client.assert_awaited_once()


@pytest.mark.asyncio
async def test_apply_expected_on_changed_unit(
    v2_client, checkin_handler, checkin_expected
):
    v2_client.component_idx = checkin_expected.component_idx  # same component
    v2_client.units = [
        Unit(
            unit_id=checkin_expected.units[0].id,
            config_idx=checkin_expected.units[0].config_state_idx - 1,
        )
    ]  # changed unit
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    await checkin_service.apply_expected(checkin_expected)

    # syncup happens
    v2_client.sync_component.assert_called_once()
    v2_client.sync_units.assert_called_once()
    checkin_handler.apply_from_client.assert_awaited_once()


@pytest.mark.asyncio
async def test_apply_expected_on_added_unit(
    v2_client, checkin_handler, checkin_expected, additional_unit
):
    v2_client.component_idx = checkin_expected.component_idx  # same component
    v2_client.units = [
        Unit(
            unit_id=checkin_expected.units[0].id,
            config_idx=checkin_expected.units[0].config_state_idx,
        )
    ]  # same unit
    checkin_expected.units.append(additional_unit)  # but there's another unit
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    await checkin_service.apply_expected(checkin_expected)

    # syncup happens
    v2_client.sync_component.assert_called_once()
    v2_client.sync_units.assert_called_once()
    checkin_handler.apply_from_client.assert_awaited_once()


@pytest.mark.asyncio
async def test_apply_expected_on_removed_unit(
    v2_client, checkin_handler, checkin_expected
):
    v2_client.component_idx = checkin_expected.component_idx  # same component
    v2_client.units = [
        Unit(
            unit_id=checkin_expected.units[0].id,
            config_idx=checkin_expected.units[0].config_state_idx,
        )
    ]  # same unit
    checkin_expected.units.pop()  # but the expected units are removed
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    await checkin_service.apply_expected(checkin_expected)

    # syncup happens
    v2_client.sync_component.assert_called_once()
    v2_client.sync_units.assert_called_once()
    checkin_handler.apply_from_client.assert_awaited_once()


@pytest.mark.asyncio
async def test_apply_expected_when_no_change(
    v2_client, checkin_handler, checkin_expected
):
    v2_client.component_idx = checkin_expected.component_idx  # same component
    v2_client.units = [
        Unit(
            unit_id=checkin_expected.units[0].id,
            config_idx=checkin_expected.units[0].config_state_idx,
            log_level=checkin_expected.units[0].log_level,
        )
    ]  # same unit
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    await checkin_service.apply_expected(checkin_expected)

    # syncup does not happen
    v2_client.sync_component.assert_not_called()
    v2_client.sync_units.assert_not_called()
    checkin_handler.apply_from_client.assert_not_awaited()


@pytest.mark.asyncio
async def test_run_starts_tasks(v2_client, checkin_handler):
    checkin_service = CheckinV2Service(v2_client, checkin_handler)

    with (
        mock.patch.object(
            checkin_service, "send_checkins", AsyncMock()
        ) as patched_send_checkins,
        mock.patch.object(
            checkin_service, "receive_checkins", AsyncMock()
        ) as patched_receive_checkins,
    ):
        await checkin_service.run()

        # We just verify that everything is called and awaited
        patched_send_checkins.assert_awaited()
        patched_receive_checkins.assert_awaited()


@pytest.mark.asyncio
async def test_run_cancels_tasks_if_any_errors_out(v2_client, checkin_handler):
    checkin_service = CheckinV2Service(v2_client, checkin_handler)

    with (
        mock.patch.object(
            checkin_service, "send_checkins", AsyncMock()
        ) as patched_send_checkins,
        mock.patch.object(
            checkin_service, "receive_checkins", AsyncMock()
        ) as patched_receive_checkins,
    ):

        async def _send_checkins(*args, **kwargs):
            # Just being lazy here:
            # We wanna make sure that this function is cancelled
            # And never reaches the end of execution
            await asyncio.sleep(60)

        class ArbitraryException(Exception):
            pass

        patched_send_checkins.side_effect = _send_checkins
        patched_receive_checkins.side_effect = ArbitraryException("Whoopsie")

        with pytest.raises(ArbitraryException):
            await checkin_service.run()


@pytest.mark.asyncio
async def test_send_checkins_run_while_service_is_running(v2_client, checkin_handler):
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    checkin_service.CHECKIN_INTERVAL = 0.1
    checkin_service.running = True

    async def _stop_checkin_service(*args, **kwargs):
        await asyncio.sleep(0.25)
        checkin_service.running = False

    with mock.patch.object(
        checkin_service, "do_checkin", AsyncMock()
    ) as patched_do_checkin:
        await asyncio.gather(
            _stop_checkin_service(), checkin_service.send_checkins(asyncio.Queue())
        )

        patched_do_checkin.assert_awaited()


@pytest.mark.asyncio
async def test_receive_checkins_run_while_service_is_running(
    v2_client, checkin_handler
):
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    checkin_service.running = True

    signal_1 = "1"
    signal_2 = "2"
    signal_3 = "3"
    stream = AsyncIterator([signal_1, signal_2, signal_3])

    with mock.patch.object(
        checkin_service, "apply_expected", AsyncMock()
    ) as patched_apply_expected:
        await checkin_service.receive_checkins(stream)

        patched_apply_expected.assert_has_calls(
            [call(signal_1), call(signal_2), call(signal_3)]
        )

@pytest.mark.asyncio
async def test_stop_successfully_stops_service(
    v2_client, checkin_handler
):
    checkin_service = CheckinV2Service(v2_client, checkin_handler)
    checkin_service.CHECKIN_INTERVAL=0.1

    async def _stop_checkin_service(*args, **kwargs):
        await asyncio.sleep(0.25)
        checkin_service.stop()

    with (
        mock.patch.object(
            checkin_service, "do_checkin", AsyncMock()
        ) as patched_do_checkin,
        mock.patch.object(
            checkin_service, "apply_expected", AsyncMock()
        ) as patched_apply_expected,
    ):
        await asyncio.gather(
            _stop_checkin_service(), checkin_service.run()
        )
