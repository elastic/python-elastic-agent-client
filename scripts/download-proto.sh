#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License 2.0;
# you may not use this file except in compliance with the Elastic License 2.0.
#
#!/bin/bash
set -x

source scripts/proto-common.sh

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
