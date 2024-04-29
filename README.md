# Python Elastic Agent client

Looking for the [main Elastic Agent client (GoLang)](https://github.com/elastic/elastic-agent-client)?

This is a python implementation, and is a technical preview.

### Using an example

This isn't actually built yet.
But the _idea_ would be:
1. compile `es_agent_client/examples/fake/component.py` (maybe with a `make` target?)
2. drop the compiled executable and a corresponding spec file into an agent's `data/elastic-agent-*/components/` dir
3. modify the agent's `elastic-agent.yml` policy to specify the fake component as an input
4. profit

### Developing

To get started, run:

```shell
make clean install
```


### What's happening?

The proto definitions for Elastic Agent live in the GoLang implementation repo.
To avoid duplicate code, they are not checked in here.
Instead, when `make generate` runs, it will:
1. download the raw `*.proto` files from the GoLang repo
2. use `grpc_tools.protoc` to generate python code from those specs
3. store that generated code in `es_agent_client/generated`


### TODO List
- [ ] Translate the [Go fake component](https://github.com/elastic/elastic-agent/blob/main/pkg/component/fake/component/main.go) to python
  - [ ] Translate the necessary [Go client helpers](https://github.com/elastic/elastic-agent-client/tree/main/pkg/client) to python
- [ ] figure out how to compile this project into an executable binary
- [ ] write tests
- [ ] add autoformatting and linting
- [ ] add CI
- [ ] record a demo
- [ ] write a blog