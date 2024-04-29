#!/bin/bash

rm es_agent_client/generated/elastic_agent*.py*

bin/python -m grpc_tools.protoc \
  -I./.proto \
  --python_out=./es_agent_client/generated \
  --pyi_out=./es_agent_client/generated \
  --grpc_python_out=./es_agent_client/generated \
  ./.proto/elastic-agent-client-deprecated.proto \
  ./.proto/elastic-agent-client.proto