is_pr() {
  if [ -z "$BUILDKITE_PULL_REQUEST" ] || [ "$BUILDKITE_PULL_REQUEST" = "false" ]; then
    echo "Running against a non-PR change"
    return 1 # false
  else
    echo "Running against a PR"
    return 0 # true
  fi
}

is_fork() {
  if [ "$BUILDKITE_PULL_REQUEST_REPO" = "git://github.com/elastic/python-elastic-agent-client.git" ] || [ "$BUILDKITE_PULL_REQUEST_REPO" = "https://github.com/elastic/python-elastic-agent-client.git" ]; then
    echo "Running against real python-elastic-agent-client repo"
    return 1 # false
  else
    echo "Running against a fork"
    return 0 # true
  fi
}

has_skip_label() {
  MATCH="ci:skip-autofix"

  IFS=',' read -ra labels <<< "${GITHUB_PR_LABELS:-}"

  for label in "${labels[@]:-}"
  do
    if [ "$label" == "$MATCH" ]; then
      echo "Found $MATCH label"
      return 0 # true
    fi
    echo "Didn't find $MATCH label"
  done

  return 1 # false
}
