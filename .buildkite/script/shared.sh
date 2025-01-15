retry() {
  local retries=$1; shift
  local delay=$1; shift
  local attempts=1

  until "$@"; do
    retry_exit_status=$?
    echo "Exited with $retry_exit_status" >&2
    if (( retries == "0" )); then
      return $retry_exit_status
    elif (( attempts == retries )); then
      echo "Failed $attempts retries" >&2
      return $retry_exit_status
    else
      echo "Retrying $((retries - attempts)) more times..." >&2
      attempts=$((attempts + 1))
      sleep "$delay"
    fi
  done
}

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
  if [ "$BUILDKITE_PULL_REQUEST_REPO" = "git://github.com/elastic/python-elastic-agent-client.git" ]; then
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
      return
    fi
  done
}
