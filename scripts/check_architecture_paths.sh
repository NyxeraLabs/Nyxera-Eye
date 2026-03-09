#!/usr/bin/env sh
# Copyright (c) 2026 NyxeraLabs
# Author: José María Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 → Apache-2.0
#
# You may:
# ✔ Study
# ✔ Modify
# ✔ Use for internal security testing
#
# You may NOT:
# ✘ Offer as a commercial service
# ✘ Sell derived competing products

set -eu

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This check must run inside a git worktree."
  exit 1
fi

BASE_REF="${1:-origin/dev}"

if git rev-parse --verify "${BASE_REF}" >/dev/null 2>&1; then
  RANGE="${BASE_REF}...HEAD"
else
  RANGE="HEAD"
fi

CHANGED_FILES="$(git diff --name-only "${RANGE}" || true)"

if [ -z "${CHANGED_FILES}" ]; then
  echo "No changed files detected for architecture path check."
  exit 0
fi

VIOLATIONS="$(printf '%s\n' "${CHANGED_FILES}" | grep -E '^(src/|frontend/|config/|infra/)' || true)"

if [ -n "${VIOLATIONS}" ]; then
  echo "Architecture path guard failed."
  echo "Sprint 22+ roadmap work must target cmd/, internal/, web/, configs/, or deployments/."
  echo "Legacy-path changes detected:"
  printf '%s\n' "${VIOLATIONS}"
  exit 1
fi

echo "Architecture path guard passed."
