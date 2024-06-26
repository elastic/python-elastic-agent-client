import tempfile
from unittest.mock import Mock, patch

from pytest import fixture, mark

import es_agent_client.generated.elastic_agent_client_pb2 as proto
from es_agent_client.client import V2Options, VersionInfo
from es_agent_client.reader import new_v2_from_reader
from es_agent_client.util.logger import logger


@fixture
def input_stream():
    startup_info = proto.StartUpInfo(
        addr="http://acme.com:1234",
        server_name="Server Name",
        token="1234",
        ca_cert=b"ca_cert",
        peer_cert=b"peer_cert",
        peer_key=b"peer_key",
        services=[],
        supports=[],
        max_message_size=1000,
        agent_info=proto.AgentInfo(
            id="1", version="1", snapshot=False, mode=proto.AgentManagedMode.STANDALONE
        ),
    )
    tmp = tempfile.NamedTemporaryFile()
    tmp.write(startup_info.SerializePartialToString(deterministic=True))
    logger.info(f"Writing StartupInfo to tmpfile: {tmp.file}")
    tmp.seek(0)
    return tmp


@fixture
def v2_options():
    return V2Options(max_message_size=100, chunking_allowed=False)


@fixture
def version_info():
    return VersionInfo(name="Test", meta=None, build_hash=None)


@mark.asyncio
@patch("grpc.ssl_channel_credentials", Mock())
@patch("grpc.aio.secure_channel", Mock())
async def test_new_v2_from_reader(input_stream, version_info, v2_options):
    try:
        v2_client = new_v2_from_reader(input_stream, ver=version_info, opts=v2_options)
        assert (
            str(v2_client)
            == "V2 Client: (agent id: 1, agent version: 1, name: Test, target: http://acme.com:1234)"
        )
    finally:
        input_stream.close()
