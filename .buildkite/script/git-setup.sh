#!/bin/bash
set -ex

if [ -z "${GITHUB_PR_BRANCH}" ]; then
  export GIT_BRANCH=${BUILDKITE_BRANCH}
else
  export GIT_BRANCH=${GITHUB_PR_BRANCH}
fi

git switch -
git checkout $GIT_BRANCH
git pull origin $GIT_BRANCH
git config --local user.email 'elasticmachine@users.noreply.github.com'
git config --local user.name 'Elastic Machine'
