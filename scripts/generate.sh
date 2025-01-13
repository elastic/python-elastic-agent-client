#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
#!/bin/bash
set -x


source ./scripts/proto-common.sh
GEN_PY_DIR="elastic_agent_client/generated"

rm ./elastic_agent_client/generated/elastic_agent*.py*

bin/python -m grpc_tools.protoc \
  -I ${PROTO_DIR} \
  --python_out=./${GEN_PY_DIR} \
  --pyi_out=./${GEN_PY_DIR} \
  --grpc_python_out=./${GEN_PY_DIR} \
  ${PROTO_DIR}/*.proto

# fix stupid imports
SED_CMD1='s/import elastic_agent_client_deprecated_pb2/from . import elastic_agent_client_deprecated_pb2/g'
sed -i.bak "$SED_CMD1" "${GEN_PY_DIR}/elastic_agent_client_pb2.py"
sed -i.bak "$SED_CMD1" "${GEN_PY_DIR}/elastic_agent_client_pb2_grpc.py"

SED_CMD2='s/import elastic_agent_client_pb2/from . import elastic_agent_client_pb2/g'
sed -i.bak "$SED_CMD2" "${GEN_PY_DIR}/elastic_agent_client_pb2_grpc.py"
sed -i.bak "$SED_CMD2" "${GEN_PY_DIR}/elastic_agent_client_future_pb2.py"

SED_CMD3='s/import elastic_agent_client_future_pb2/from . import elastic_agent_client_future_pb2/g'
sed -i.bak "$SED_CMD3" "${GEN_PY_DIR}/elastic_agent_client_future_pb2_grpc.py"

rm ${GEN_PY_DIR}/*.bak
