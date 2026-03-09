SHELL := /bin/sh

.PHONY: help install install-poetry install-venv test compile infra-check e2e qa up down run-api frontend-install frontend-dev frontend-build deploy docs

help:
	@echo "Nyxera Eye Make Targets"
	@echo "  make install         # Install dependencies (Poetry if available, else venv)"
	@echo "  make install-poetry  # Install with Poetry"
	@echo "  make install-venv    # Install with Python venv + pip"
	@echo "  make test            # Run pytest"
	@echo "  make compile         # Compile-check Python sources"
	@echo "  make infra-check     # Validate docker compose configuration"
	@echo "  make e2e             # Run full deterministic E2E validation"
	@echo "  make qa              # Run compile + infra-check + e2e"
	@echo "  make up              # Start infrastructure stack"
	@echo "  make down            # Stop infrastructure stack"
	@echo "  make run-api         # Run FastAPI app locally"
	@echo "  make frontend-install# Install frontend dependencies"
	@echo "  make frontend-dev    # Run Next.js frontend dev server"
	@echo "  make frontend-build  # Build frontend production bundle"
	@echo "  make deploy          # Start infra + API and print frontend instructions"
	@echo "  make docs            # Print docs entry points"

install:
	@if command -v poetry >/dev/null 2>&1; then \
		$(MAKE) install-poetry; \
	else \
		$(MAKE) install-venv; \
	fi

install-poetry:
	poetry install --no-interaction

install-venv:
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip && pip install pytest fastapi httpx arq

test:
	@if command -v poetry >/dev/null 2>&1; then \
		poetry run pytest -q; \
	else \
		PYTHONPATH=src python -m pytest -q; \
	fi

compile:
	python -m compileall -q src tests scripts

infra-check:
	docker compose config -q

e2e:
	PYTHONPATH=src python scripts/e2e_full_validation.py

qa: compile infra-check e2e

up:
	docker compose up -d

down:
	docker compose down

run-api:
	PYTHONPATH=src uvicorn nyxera_eye.api.app:app --host 127.0.0.1 --port 8000

frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

deploy: up
	@echo "Infrastructure started."
	@echo "Run API: make run-api"
	@echo "Run frontend: make frontend-dev"

docs:
	@echo "Manuals index: docs/manuals/INDEX.md"
	@echo "Runbook: docs/RUNBOOK.md"
	@echo "Dev logs index: docs/dev-logs/INDEX.md"
	@echo "Roadmap: docs/ROADMAP.md"
