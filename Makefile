.PHONY: install

PYTHON=python3.10
COVERAGE_THRESHOLD=0 # percents
SLOW_TEST_THRESHOLD=1 # seconds

ES_HOST?=http://127.0.0.1:9200
ES_USERNAME?=elastic
ES_PASSWORD?=changeme

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

lint: dev
	bin/mypy -p es_agent_client
	bin/ruff es_agent_client
	bin/pyright es_agent_client
	bin/ruff tests
	bin/pyright tests

autoformat: dev
	bin/black es_agent_client --exclude generated
	bin/black tests
	bin/ruff es_agent_client --fix
	bin/ruff tests --fix

test: dev install
	bin/pytest --cov-report term-missing --cov-fail-under $(COVERAGE_THRESHOLD) --cov-report html --cov=es_agent_client --fail-slow=$(SLOW_TEST_THRESHOLD) -sv tests

clean:
	rm -rf bin lib include .proto

docker-build:
	docker build -t python-test-agent .

docker-run:
	docker run \
		--env ELASTICSEARCH_HOSTS=$(ES_HOST) \
		--env ELASTICSEARCH_USERNAME=$(ES_USERNAME) \
		--env ELASTICSEARCH_PASSWORD=$(ES_PASSWORD) \
		python-test-agent

docker-all: docker-build docker-run
