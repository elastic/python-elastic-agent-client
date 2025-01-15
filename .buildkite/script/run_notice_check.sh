#!/bin/bash

# !!! WARNING DO NOT add -x to avoid leaking vault passwords
set -euo pipefail

source .buildkite/script/shared.sh

make notice

if [ -z "$(git status --porcelain | grep NOTICE.txt)" ]; then
  echo 'Nothing changed'
  exit 0
else 
  echo 'New changes to NOTICE.txt:'
  git --no-pager diff
  if is_pr && ! is_fork && !has_skip_label; then
    echo 'Running on a PR that is not a fork, will commit changes'
    source .buildkite/script/git-setup.sh
    export GH_TOKEN="$VAULT_GITHUB_TOKEN"

    git add NOTICE.txt
    git commit -m"Update NOTICE.txt"
    git push
    sleep 15
  else
    echo 'Skipping autofix'
  fi

  exit 1
fi

exit 0
