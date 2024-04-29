# Python Elastic Agent client

Looking for the [main Elastic Agent client (GoLang)](https://github.com/elastic/elastic-agent-client)?

This is a python implementation, and is a technical preview.

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


