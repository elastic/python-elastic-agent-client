#!/bin/bash

# !!! WARNING DO NOT add -x to avoid leaking vault passwords
set -euo pipefail

source .buildkite/scripts/shared.sh
source .buildkite/scripts/git-setup.sh

make generate

if [ -z "$(git status --porcelain | grep elastic_agent_client/generated)" ]; then
  exit 0
else 
  if is_pr; then
    export GH_TOKEN="$VAULT_GITHUB_TOKEN"

    git add elastic_agent_client/generated
    git commit -m"Update protobuf files"
    git push
  fi

  exit 1
fi

exit 0


