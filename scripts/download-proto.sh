#!/bin/bash

PROTO_DIR=".proto/"
PROTO_SRC="https://raw.githubusercontent.com/elastic/elastic-agent-client/main/elastic-agent-client.proto"
DEPRECATED_PROTO_SRC="https://raw.githubusercontent.com/elastic/elastic-agent-client/main/elastic-agent-client-deprecated.proto"
OUTPUT_FILE="elastic-agent-client.proto"
DEPRECATED_OUTPUT_FILE="elastic-agent-client-deprecated.proto"

rm -rf $PROTO_DIR
mkdir -p $PROTO_DIR

curl -L -o $PROTO_DIR/$OUTPUT_FILE $PROTO_SRC
curl -L -o $PROTO_DIR/$DEPRECATED_OUTPUT_FILE $DEPRECATED_PROTO_SRC

