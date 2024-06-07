.PHONY: install

PYTHON=python3.10

bin/python:
	$(PYTHON) -m venv .
	bin/pip install --upgrade pip

dev: bin/python
	bin/pip install -r requirements.txt

generate: bin/python dev
	./scripts/download-proto.sh
	./scripts/generate.sh

install: bin/python
	bin/pip install -e .

exe: dev
	bin/pyoxidizer build

clean:
	rm -rf bin lib include .proto build