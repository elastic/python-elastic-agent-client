.PHONY: install

PYTHON=python3.10
COVERAGE_THRESHOLD=0 # percents
SLOW_TEST_THRESHOLD=1 # seconds

bin/python:
	$(PYTHON) -m venv .
	bin/pip install --upgrade pip

dev: bin/python
	bin/pip install -r requirements/lib.txt -r requirements/dev.txt

generate: bin/python dev
	./scripts/download-proto.sh
	./scripts/generate.sh

install: bin/python
	bin/pip install -e .

lint: dev
	bin/mypy -p es_agent_client
	bin/ruff check es_agent_client
	bin/pyright es_agent_client
	bin/ruff check tests
	bin/pyright tests

autoformat: dev
	bin/black es_agent_client --exclude generated
	bin/black tests
	bin/ruff check es_agent_client --fix
	bin/ruff check tests --fix

test: dev install
	bin/pytest --cov-report term-missing --cov-fail-under $(COVERAGE_THRESHOLD) --cov-report html --cov=es_agent_client --fail-slow=$(SLOW_TEST_THRESHOLD) -sv tests

clean:
	rm -rf bin lib include .proto
