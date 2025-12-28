#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_DIR="${ROOT}/.venv"
REQS_FILE="${ROOT}/requirements.txt"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required but not found on PATH. Install from https://github.com/astral-sh/uv" >&2
  exit 1
fi

echo "Creating virtual environment at ${ENV_DIR}..."
uv venv "${ENV_DIR}"

echo "Installing requirements from ${REQS_FILE}..."
uv pip install -r "${REQS_FILE}" --python "${ENV_DIR}/bin/python"

echo "Done. Activate with: source ${ENV_DIR}/bin/activate"
