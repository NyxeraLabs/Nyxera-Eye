SHELL := /bin/sh

API_HOST ?= 127.0.0.1
API_PORT ?= 18080
FRONTEND_HOST ?= 127.0.0.1
FRONTEND_PORT ?= 3001
VENV_DIR ?= .venv
PYTHON ?= python3
VENV_PY := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_PY) -m pip

.PHONY: help install install-poetry install-venv ensure-venv test compile infra-check e2e qa up down run-api frontend-install frontend-dev frontend-build nginx-certs deploy docs run-all stop-all status-all audit-tail

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
	@echo "  make run-api         # Run FastAPI app locally via .venv"
	@echo "  make frontend-install# Install frontend dependencies"
	@echo "  make frontend-dev    # Run Next.js frontend dev server"
	@echo "  make frontend-build  # Build frontend production bundle"
	@echo "  make nginx-certs     # Generate local self-signed TLS certs for nginx"
	@echo "  make deploy          # Start full dockerized stack (infra + api + frontend)"
	@echo "  make run-all         # Alias of deploy"
	@echo "  make stop-all        # Stop full dockerized stack"
	@echo "  make status-all      # Show running container status"
	@echo "  make audit-tail      # Tail backend audit ledger events"
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
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_PIP) install --upgrade pip setuptools wheel
	$(VENV_PIP) install -e .
	$(VENV_PIP) install pytest

ensure-venv:
	@if [ ! -x "$(VENV_PY)" ]; then \
		echo "Creating local virtualenv under $(VENV_DIR)/"; \
		$(MAKE) install-venv; \
	fi
	@if ! $(VENV_PY) -c "import uvicorn" >/dev/null 2>&1; then \
		echo "Installing local runtime deps in $(VENV_DIR)/..."; \
		$(VENV_PIP) install -e . pytest; \
	fi

test:
	@if command -v poetry >/dev/null 2>&1; then \
		poetry run pytest -q; \
	else \
		$(MAKE) ensure-venv; \
		PYTHONPATH=src $(VENV_PY) -m pytest -q; \
	fi

compile:
	@if command -v poetry >/dev/null 2>&1; then \
		poetry run python -m compileall -q src tests scripts; \
	else \
		$(MAKE) ensure-venv; \
		$(VENV_PY) -m compileall -q src tests scripts; \
	fi

infra-check:
	docker compose config -q

e2e:
	@if command -v poetry >/dev/null 2>&1; then \
		poetry run env PYTHONPATH=src python scripts/e2e_full_validation.py; \
	else \
		$(MAKE) ensure-venv; \
		PYTHONPATH=src $(VENV_PY) scripts/e2e_full_validation.py; \
	fi

qa: compile infra-check e2e

up:
	docker compose up -d --build

down:
	docker compose down

run-api: ensure-venv
	NYXERA_AUTH_ADMIN_USER=$${NYXERA_AUTH_ADMIN_USER:-admin} NYXERA_AUTH_ADMIN_PASSWORD=$${NYXERA_AUTH_ADMIN_PASSWORD:-admin-change-me} PYTHONPATH=src $(VENV_PY) -m uvicorn nyxera_eye.api.app:app --host $(API_HOST) --port $(API_PORT)

frontend-install:
	cd frontend && npm install

frontend-dev:
	@if [ ! -x frontend/node_modules/.bin/next ]; then \
		echo "Frontend dependencies not found. Installing..."; \
		$(MAKE) frontend-install; \
	fi
	cd frontend && npm run dev -- --hostname $(FRONTEND_HOST) -p $(FRONTEND_PORT)

frontend-build:
	@if [ ! -x frontend/node_modules/.bin/next ]; then \
		echo "Frontend dependencies not found. Installing..."; \
		$(MAKE) frontend-install; \
	fi
	cd frontend && npm run build

nginx-certs:
	@mkdir -p config/nginx/certs
	@openssl req -x509 -nodes -newkey rsa:2048 \
		-keyout config/nginx/certs/nyxera.key \
		-out config/nginx/certs/nyxera.crt \
		-days 3650 \
		-subj "/C=US/ST=Local/L=Local/O=Nyxera/CN=127.0.0.1"
	@echo "Generated local TLS certs under config/nginx/certs/"

deploy: nginx-certs up
	@echo "Infrastructure started."
	@echo "API docs: https://127.0.0.1:8448/api/docs"
	@echo "Frontend: https://127.0.0.1:8449"

run-all: deploy

stop-all:
	docker compose down

status-all:
	docker compose ps

audit-tail:
	@mkdir -p .run
	@touch .run/audit-events.jsonl
	tail -f .run/audit-events.jsonl

docs:
	@echo "Manuals index: docs/manuals/INDEX.md"
	@echo "Runbook: docs/RUNBOOK.md"
	@echo "Dev logs index: docs/dev-logs/INDEX.md"
	@echo "Audit log (runtime): .run/audit-events.jsonl"
	@echo "Roadmap: docs/ROADMAP.md"
