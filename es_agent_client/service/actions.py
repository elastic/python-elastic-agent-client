import asyncio
import functools
import json

import es_agent_client.generated.elastic_agent_client_pb2 as proto

from es_agent_client.util.async_tools import AsyncQueueIterator, BaseService
from es_agent_client.client import V2
from es_agent_client.util.logger import logger
from google.protobuf.json_format import MessageToJson


class ActionsService(BaseService):
    name = "actions"

    def __init__(self, client: V2, action_handler):
        super().__init__(client, "actions")
        logger.info("Initializing the actions service")
        self.client = client
        self.action_handler = action_handler

    async def _run(self):
        send_queue = asyncio.Queue()
        action_stream = self.client.client.Actions(AsyncQueueIterator(send_queue))
        logger.info("Sending startup action event")
        await send_queue.put(proto.ActionResponse(
            token=self.client.token,
            id="init",
            status=proto.ActionResponse.SUCCESS,
            result=self.init_action_result()
        ))

        logger.info("Listening for action events...")
        action: proto.ActionRequest
        async for action in action_stream:
            action_str = json.dumps(json.loads(MessageToJson(action))) # TODO, this is super inefficient and should be removed
            logger.info(f"received a action event from actionV2: {action_str}")
            try:
                functools.partial(self.action_handler, action)()
            except Exception as e:
                logger.exception(f"Failed to do action: {action}", e)
                await send_queue.put(proto.ActionResponse(
                    token=self.client.token,
                    id=action.id,
                    status=proto.ActionResponse.FAILED,
                    result=self.generic_action_failure()
                ))

    def init_action_result(self):
        return json.dumps({}).encode()

    def generic_action_failure(self):
        return json.dumps({"error": "Action failed"}).encode()

