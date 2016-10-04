.SILENT:
PYTHON=$(shell which python)
PIP=venv/bin/pip
PYTEST=venv/bin/py.test

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
	 MONK_TEST=True
	 MONK_REDIS_HOST=localhost\
	 MONK_REDIS_PORT=6379\
	 MONK_REDIS_DB=0\
	 PYTHONPATH=.\
	 ${PYTEST} tests/ -s -r a --color=yes -vvv

task: clean
	PYTHONPATH=. ${PYTHON} tasks.py

container-worker:
	docker exec -it monk-worker bash

container-redis:
	docker exec -it monk-redis redis-cli

clean-redis:
	docker exec -it monk-redis redis-cli flushall
