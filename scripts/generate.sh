#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
#!/bin/bash
set -x


PROTO_DIR=".proto"
ELASTIC_AGENT_CLIENT="elastic-agent-client"
ELASTIC_AGENT_CLIENT_DEPRECATED="elastic-agent-client-deprecated"
ELASTIC_AGENT_CLIENT_FUTURE="elastic-agent-client-future"
GEN_PY_DIR="elastic_agent_client/generated"

# Download
PROTO_SRC="https://raw.githubusercontent.com/elastic/elastic-agent-client/main/${ELASTIC_AGENT_CLIENT}.proto"
DEPRECATED_PROTO_SRC="https://raw.githubusercontent.com/elastic/elastic-agent-client/main/${ELASTIC_AGENT_CLIENT_DEPRECATED}.proto"
FUTURE_PROTO_SRC="https://raw.githubusercontent.com/elastic/elastic-agent-client/main/${ELASTIC_AGENT_CLIENT_FUTURE}.proto"
OUTPUT_FILE="${ELASTIC_AGENT_CLIENT}.proto"
DEPRECATED_OUTPUT_FILE="${ELASTIC_AGENT_CLIENT_DEPRECATED}.proto"
FUTURE_OUTPUT_FILE="${ELASTIC_AGENT_CLIENT_FUTURE}.proto"

rm -rf $PROTO_DIR
mkdir -p ${PROTO_DIR}

curl -L -o $PROTO_DIR/$OUTPUT_FILE ${PROTO_SRC}
curl -L -o $PROTO_DIR/$DEPRECATED_OUTPUT_FILE ${DEPRECATED_PROTO_SRC}
curl -L -o $PROTO_DIR/$FUTURE_OUTPUT_FILE ${FUTURE_PROTO_SRC}


# Generate
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
