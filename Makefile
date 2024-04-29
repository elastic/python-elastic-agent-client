.PHONY: install

PYTHON=python3.10

bin/python:
	$(PYTHON) -m venv .
	bin/pip install --upgrade pip
	bin/pip install -r requirements.txt

generate: bin/python
	./scripts/download-proto.sh
	./scripts/generate.sh

install: bin/python generate
	bin/pip install -e .

clean:
	rm -rf bin lib include .proto