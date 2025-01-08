# Publishing a package to pypi

This guide explains how to publish the package into PyPi: https://pypi.org/project/elastic-agent-client/.

## Versioning strategy

For now we'll stick with a simple strategy of having `0.1.0` release and then bump patch versions: `0.1.1`, `0.1.2`, `0.1.3` and so on. Once we feel package is ready for proper public release we will choose a versioning strategy similar to other Elastic products and will stick to it.

## Getting credentials

You will need `vault` CLI tools installed or have access to a web version. You need to have permissions to access the keys - if you don't please reach out to the team lead.

Secrets for publishing to live PyPi are in `ent-search-team/pypi-ent-search-dev`, secrets for publishing to test version are in `ent-search-team/test-pypi-ent-search-dev`.

## Actually publishing

1. First make sure that the version of the package (see https://github.com/elastic/python-elastic-agent-client/blob/main/elastic_agent_client/version.py) is correct and is the desired version number
2. Verify that all linting and tests pass: `make lint test`
3. Verify that protobuf files are up-to-date: `make generate` and then `git diff` to see the changes. If any changes are present, first merge them into the branch published before continuing
4. Do a test publish: `make test-release`. When prompted for an api key, insert a key from running this command: `vault read -field publishing-api-key secret/ent-search-team/test-pypi-ent-search-dev`
5. Check the package on https://test.pypi.org/project/elastic-agent-client - check readme, version, other things that you consider important
6. Do a prod publish: `make release`. When prompted for an api key, insert a key from running this command: `vault read -field publishing-api-key secret/ent-search-team/pypi-ent-search-dev`
7. Check the package on https://pypi.org/project/elastic-agent-client - check readme, version, other things that you consider important
8. Bump version in the version file: https://github.com/elastic/python-elastic-agent-client/blob/main/elastic_agent_client/version.py
9. Done!
