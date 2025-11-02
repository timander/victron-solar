# Makefile for victron-python

.PHONY: install test lint run clean

install:
	pip install -e .[test]

test:
	pytest tests/

lint:
	flake8 victron/

run:
	python -m victron.pipeline

clean:
	rm -rf __pycache__ .pytest_cache
