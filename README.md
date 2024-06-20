# Python Elastic Agent client

Looking for the [main Elastic Agent client (GoLang)](https://github.com/elastic/elastic-agent-client)?

This is a python implementation, and is a technical preview.

### Using an example

Agent needs a binary to run.
A simple executable shell script will do.

```shell
#!/bin/bash
PYTHON_PATH=/path/to/bin/python
PY_AGENT_CLIENT_PATH=/path/to/python-elastic-agent-client
$PYTHON_PATH $PY_AGENT_CLIENT_PATH/es_agent_client/examples/fake/component.py
```

Put those contents in a `elastic-agent*/data/elastic-agent*/components/python-elastic-agent-client` file, and
```shell
chmod 755 elastic-agent*/data/elastic-agent*/components/python-elastic-agent-client
```

You'll also need to create a specfile at `elastic-agent*/data/elastic-agent*/components/python-elastic-agent-client.spec.yml`
with the contents:
```yaml
version: 2
inputs:
  - name: fake-py
    description: "Fake Py component input"
    platforms: &platforms
      - linux/amd64
      - linux/arm64
      - darwin/amd64
      - darwin/arm64
      - windows/amd64
      - container/amd64
      - container/arm64
    outputs: &outputs
      - elasticsearch
    shippers: &shippers
      - shipper
    command: &command
      restart_monitoring_period: 5s
      maximum_restarts_per_period: 1
      timeouts:
        restart: 1s
      args: []
```

Then use this input in your `elastic-agent.yml` with:
```
inputs:
  - type: fake-py
    id: fake-py
    use_output: default
```

You can easily tail the logs by running:
```
sudo ./elastic-agent 2>&1 >/dev/null  | jq '.message'
```

### Developing

To get started, run:

```shell
make clean install
```


### What's happening?

##### Protobuf

The proto definitions for Elastic Agent live in the GoLang implementation repo.
To avoid duplicate code, they are not checked in here.
Instead, when `make generate` runs, it will:
1. download the raw `*.proto` files from the GoLang repo
2. use `grpc_tools.protoc` to generate python code from those specs
3. store that generated code in `es_agent_client/generated`
4. post-process them a bit (grpc_tools generates python2 imports, instead of python3 🤷)



### TODO List
- [ ] Translate the [Go fake component](https://github.com/elastic/elastic-agent/blob/main/pkg/component/fake/component/main.go) to python
  - [ ] Translate the necessary [Go client helpers](https://github.com/elastic/elastic-agent-client/tree/main/pkg/client) to python
- [ ] introduce pyinstaller? [thread](https://elastic.slack.com/archives/CTE3Q1MFG/p1717780247032599?thread_ts=1717776309.734889&cid=CTE3Q1MFG)
- [ ] remove all inline TODOs
- [ ] write tests
- [ ] add autoformatting and linting
- [ ] use ECS logging
- [ ] add CI
- [ ] add NOTICE file
- [ ] open source
- [ ] record a demo
- [ ] write a blog