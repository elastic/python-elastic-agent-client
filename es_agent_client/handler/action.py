import es_agent_client.generated.elastic_agent_client_pb2 as proto


class BaseActionHandler:

    async def handle_action(self, action: proto.ActionRequest):
        raise NotImplementedError()
