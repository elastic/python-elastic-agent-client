from elastic_agent_client.client import V2


class BaseCheckinHandler:
    def __init__(self, client: V2):
        self.client = client

    async def apply_from_client(self):
        raise NotImplementedError()
