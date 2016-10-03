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

test:clean
	 PYTHONPATH=. ${PYTEST} tests/ -s -r a --color=yes -vvv

run: clean
	 PYTHONPATH=. ${PYTHON} main.py
