import asyncio
from unittest.mock import Mock

import pytest

import es_agent_client.generated.elastic_agent_client_pb2 as proto
from es_agent_client.client import V2, Unit, VersionInfo
from es_agent_client.service.checkin import CheckinV2Service


@pytest.fixture
def checkin_handler():
    checkin_handler = Mock()
    checkin_handler.apply_from_client = Mock()
    return checkin_handler


@pytest.fixture
def v2_client():
    v2_client = V2()
    v2_client.client = Mock()
    v2_client.client.CheckinV2 = Mock()
    return v2_client


@pytest.mark.asyncio
async def test_error_on_unset_stub(checkin_handler):
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
