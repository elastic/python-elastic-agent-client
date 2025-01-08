#!/bin/bash

# !!! WARNING DO NOT add -x to avoid leaking vault passwords
set -euo pipefail

source .buildkite/scripts/shared.sh
source .buildkite/scripts/git-setup.sh

make notice

if [ -z "$(git status --porcelain | grep NOTICE.txt)" ]; then
  exit 0
else 
  if is_pr; then
    export GH_TOKEN="$VAULT_GITHUB_TOKEN"

    git add NOTICE.txt
    git commit -m"Update NOTICE.txt"
    git push
  fi

  exit 1
fi

exit 0

