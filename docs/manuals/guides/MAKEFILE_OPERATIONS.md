# Makefile Operations Guide

## Purpose

Use `Makefile` targets to standardize install, validation, and local deployment tasks.

## Common Commands

```bash
make help
make install
make compile
make test
make infra-check
make e2e
make qa
make up
make down
make run-api
```

## Typical QA Flow

```bash
make install
make qa
```

## Typical Local Runtime Flow

```bash
make up
make run-api
```

In a separate shell:

```bash
curl -s http://127.0.0.1:8000/health
```

Stop infrastructure when done:

```bash
make down
```
