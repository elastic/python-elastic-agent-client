#!/bin/bash

# !!! WARNING DO NOT add -x to avoid leaking vault passwords
set -euo pipefail

source .buildkite/script/shared.sh

if is_pr && ! is_fork && ! has_skip_label; then
  echo "We're on PR, running autoformat"

  export GH_TOKEN="$VAULT_GITHUB_TOKEN"
  source .buildkite/script/git-setup.sh

  if ! make autoformat ; then
    echo "make autoformat ran with errors, exiting"
    exit 1
  fi

  if [ -z "$(git status --porcelain)" ]; then
    echo "Nothing to be fixed by autoformat"
    exit 0
  else
    git --no-pager diff
    echo "linting errors are fixed, pushing the diff"

    git add .
    git commit -m"make autoformat"
    git push
    # exit 1 to re-trigger the build
    exit 1
  fi
else
  echo "Skipping autofix, running only linter"
  # On non-PR branches the bot has no permissions to open PRs.
  # Theoretically this would never fail because we always ask
  # linter to succeed to merge. It can fail intermittently?
  make lint
fi
