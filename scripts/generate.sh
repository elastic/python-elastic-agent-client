#!/bin/bash
set -x
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source ${SCRIPT_DIR}/proto-common.sh

rm es_agent_client/generated/elastic_agent*.py*

bin/python -m grpc_tools.protoc \
  -I ${PROTO_DIR} \
  --python_out=./es_agent_client/generated \
  --pyi_out=./es_agent_client/generated \
  --grpc_python_out=./es_agent_client/generated \
  ${PROTO_DIR}/*.proto

# fix stupid imports
sed -i.bak 's/import elastic_agent_client_deprecated_pb2/from . import elastic_agent_client_deprecated_pb2/g' "es_agent_client/generated/elastic_agent_client_pb2.py"
rm es_agent_client/generated/elastic_agent_client_pb2.py.bak