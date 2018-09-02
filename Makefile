.SILENT:
PYTHON=$(shell which python)
PIP=venv/bin/pip
PYTEST=$(shell which py.test)

clean:
	find . \( -name *.py[co] -o -name __pycache__ \) -delete

venv:
	virtualenv venv --python=python3

setup: venv
	${PIP} install -U pip
	${PIP} install -r requirements.txt

setup-local: setup
	${PIP} install -r requirements_dev.txt

test: clean
	 MONK_TEST=True\
	 PYTHONPATH=. ${PYTEST} tests/ -s -r a --color=yes -vvv --cov=monk --cov-report term-missing

task: clean
	PYTHONPATH=. ${PYTHON} tasks.py

container-test:
	docker exec -it monk-worker make test

container-task:
	docker exec -it monk-worker make task

container-worker:
	docker exec -it monk-worker bash

container-redis:
	docker exec -it monk-redis redis-cli

clean-redis:
	docker exec -it monk-redis redis-cli flushall
