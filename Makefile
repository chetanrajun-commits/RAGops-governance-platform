.PHONY: install dev test lint run demo clean

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests

run:
	python -m ragops run --config examples/rbac-config.yaml --query "What is the Q3 layoff plan?" --role hr_manager

demo: install
	python -m ragops run --config examples/rbac-config.yaml --query "What is the Q3 layoff plan?" --role hr_manager

clean:
	rm -rf out .pytest_cache .ruff_cache **/__pycache__
