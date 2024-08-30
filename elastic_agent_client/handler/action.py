#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
import elastic_agent_client.generated.elastic_agent_client_pb2 as proto


class BaseActionHandler:
    async def handle_action(self, action: proto.ActionRequest):
        raise NotImplementedError()
