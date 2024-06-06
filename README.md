# Python Elastic Agent client

Looking for the [main Elastic Agent client (GoLang)](https://github.com/elastic/elastic-agent-client)?

This is a python implementation, and is a technical preview.

### Using an example

1. compile `es_agent_client/examples/fake/component.py` with `make exe`
2. drop the compiled executable (`build/**/debug/install/py*`) and a corresponding spec file into an agent's `data/elastic-agent-*/components/` dir
3. modify the agent's `elastic-agent.yml` policy to specify the fake component as an input
4. start agent (`sudo ./elastic-agent`)
5. see that the python agent runs (`sudo tail -f data/elastic-agent-*/log/*.log`)

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

###### PyOxidizer

Agent needs a binary that it can execute. 
A tool called [PyOxidizer](https://gregoryszorc.com/docs/pyoxidizer/main/pyoxidizer_overview.html) helps us accomplish this, by compiling an entire python distribution (including our source code and dependencies) into a single executable.
In our case, it also produces a `py_lib/` dir that must live next to that binary, which contains c extensions that can't be memoized.
These must be copied into the Agent artifact manually for now.
Eventually, these will be included in Agent's automated builds.

The binary is produced with `make exe`, and is controlled via the `pyoxidizer.bzl` configuration file.

### TODO List
- [ ] Translate the [Go fake component](https://github.com/elastic/elastic-agent/blob/main/pkg/component/fake/component/main.go) to python
  - [ ] Translate the necessary [Go client helpers](https://github.com/elastic/elastic-agent-client/tree/main/pkg/client) to python
- [ ] write tests
- [ ] add autoformatting and linting
- [ ] add CI
- [ ] record a demo
- [ ] write a blog