.PHONY: setup test lint clean

setup:
	pip install -e .
	pip install pytest pytest-cov

test:
	pytest

test-cov:
	pytest --cov=enchante tests/

lint:
	ruff check .
	ruff format --check .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +

