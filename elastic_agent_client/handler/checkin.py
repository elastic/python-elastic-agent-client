#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
from elastic_agent_client.client import V2


class BaseCheckinHandler:
    def __init__(self, client: V2):
        self.client = client

    async def apply_from_client(self):
        raise NotImplementedError()
