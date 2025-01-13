#!/bin/bash

# !!! WARNING DO NOT add -x to avoid leaking vault passwords
set -euo pipefail

source .buildkite/script/shared.sh
source .buildkite/script/git-setup.sh

SCRIPT_DIR="scripts" make generate 

if [ -z "$(git status --porcelain | grep elastic_agent_client/generated)" ]; then
  exit 0
else 
  if is_pr && ! is_fork; then
    echo "Commiting changed protobuf files"
    export GH_TOKEN="$VAULT_GITHUB_TOKEN"

    git add elastic_agent_client/generated
    git commit -m"Update protobuf files"
    git push
  else
    echo "Running against a fork or non-PR change, skipping committing changes"
  fi

  exit 1
fi

exit 0


