#!/bin/bash
set -x
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source ${SCRIPT_DIR}/proto-common.sh

PROTO_SRC="https://raw.githubusercontent.com/elastic/elastic-agent-client/main/${ELASTIC_AGENT_CLIENT}.proto"
DEPRECATED_PROTO_SRC="https://raw.githubusercontent.com/elastic/elastic-agent-client/main/${ELASTIC_AGENT_CLIENT_DEPRECATED}.proto"
OUTPUT_FILE="${ELASTIC_AGENT_CLIENT}.proto"
DEPRECATED_OUTPUT_FILE="${ELASTIC_AGENT_CLIENT_DEPRECATED}.proto"

rm -rf $PROTO_DIR
mkdir -p ${PROTO_DIR}
mkdir -p ${PROTO_DIR}

curl -L -o $PROTO_DIR/$OUTPUT_FILE ${PROTO_SRC}
curl -L -o $PROTO_DIR/$DEPRECATED_OUTPUT_FILE ${DEPRECATED_PROTO_SRC}

