.PHONY: install

PYTHON=python3.10
COVERAGE_THRESHOLD=0 # percents
SLOW_TEST_THRESHOLD=1 # seconds

bin/python:
	$(PYTHON) -m venv .
	bin/pip install --upgrade pip

bin/hatch: bin/python
	bin/pip install hatch


dev: bin/python
	bin/pip install -r requirements.txt

generate: bin/python dev
	./scripts/download-proto.sh
	./scripts/generate.sh

install: bin/python
	bin/pip install -e .

build: install bin/hatch
	bin/hatch build

lint: dev
	bin/mypy -p elastic_agent_client
	bin/ruff check elastic_agent_client
	bin/pyright elastic_agent_client
	bin/ruff check tests
	bin/pyright tests

autoformat: dev
	bin/black elastic_agent_client --exclude generated
	bin/black tests
	bin/ruff check elastic_agent_client --fix
	bin/ruff check tests --fix

test: dev install
	bin/pytest --cov-report term-missing --cov-fail-under $(COVERAGE_THRESHOLD) --cov-report html --cov=elastic_agent_client --fail-slow=$(SLOW_TEST_THRESHOLD) -sv tests

clean:
	rm -rf bin lib include .proto
