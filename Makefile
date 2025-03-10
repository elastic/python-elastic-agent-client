.PHONY: install

PYTHON=python3.10
SLOW_TEST_THRESHOLD=1 # seconds

bin/python:
	$(PYTHON) -m venv .
	bin/pip install --upgrade pip

bin/hatch: dev

bin/twine: dev

dev: bin/python
	bin/pip install -r requirements.txt

notice: dev bin/python
	echo "python-elastic-agent-client" > NOTICE.txt
	echo "Copyright 2024 Elasticsearch B.V." >> NOTICE.txt
	echo "" >> NOTICE.txt
	bin/pip-licenses >> NOTICE.txt


generate: bin/python dev
	./scripts/generate.sh
	echo "Running import tests for generated files"
	bin/python -c "import elastic_agent_client.generated.elastic_agent_client_pb2"
	bin/python -c "import elastic_agent_client.generated.elastic_agent_client_future_pb2"
	bin/python -c "import elastic_agent_client.generated.elastic_agent_client_deprecated_pb2"

install: bin/python dev notice
	bin/pip install -e .

build: install bin/hatch bin/twine
	bin/hatch build

test-release: build
	bin/twine upload -r testpypi dist/*

release: clean build
	bin/twine upload dist/*

lint: dev
	bin/mypy -p elastic_agent_client
	bin/ruff check
	bin/ruff format --check

autoformat: dev
	bin/ruff check --fix
	bin/ruff format

test: dev install
	bin/pytest --cov-config=pyproject.toml --cov=. --fail-slow=$(SLOW_TEST_THRESHOLD) -sv tests

clean:
	rm -rf bin lib include .proto dist
