.PHONY: dev install run test lint format

dev:
	poetry install

install:
	poetry install --only main

run:
	poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

run-prod:
	poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

test:
	poetry run pytest

lint:
	poetry run black --check src tests
	poetry run isort --check-only src tests
	poetry run mypy src

format:
	poetry run black src tests
	poetry run isort src tests
