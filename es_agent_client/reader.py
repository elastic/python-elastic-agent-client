import grpc  # type: ignore

from es_agent_client.client import V2, V2Options
from es_agent_client.generated.elastic_agent_client_pb2 import (
    AgentInfo,
    ConnectionSupports,
    StartUpInfo,
)
from es_agent_client.generated.elastic_agent_client_pb2_grpc import ElasticAgentStub
from es_agent_client.util.logger import logger


def new_v2_from_reader(reader, ver, opts: V2Options):
    info = StartUpInfo()
    data = reader.read()  # read input
    info.ParseFromString(data)
    if info.agent_info is not None:
        opts.agent_info = AgentInfo(
            id=info.agent_info.id,
            version=info.agent_info.version,
            snapshot=info.agent_info.snapshot,
            mode=info.agent_info.mode,
        )

    if info.services is None:
        msg = "No supported services detected"
        raise RuntimeError(msg)

    for s in info.supports:
        if s == ConnectionSupports.CheckinChunking:
            opts.chunking_allowed = True

    logger.info("Setting up secure channel")

    channel_credentials = grpc.ssl_channel_credentials(
        root_certificates=info.ca_cert,
        private_key=info.peer_key,
        certificate_chain=info.peer_cert,
    )
    channel = grpc.aio.secure_channel(
        info.addr,
        channel_credentials,
        options=[("grpc.ssl_target_name_override", info.server_name)],
    )
    client = V2()
    client.target = info.addr
    client.opts = opts
    client.token = info.token
    client.agent_info = info.agent_info
    client.version_info = ver
    client.units = []
    client.client = ElasticAgentStub(channel)

    logger.info(f"Initialized V2 client: {client}")

    return client
