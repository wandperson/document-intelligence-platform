#!/usr/bin/env bash
set -euo pipefail

echo ": Checking if \`uv\` is installed..."

if ! command -v uv &>/dev/null; then
  echo "Error: \`uv\` is not installed."
  echo "Install it first: https://github.com/astral-sh/uv"
  exit 1
fi

# Find the git repository root
echo ": Finding git repository root..."
ROOT_DIR=$(git rev-parse --show-toplevel 2>/dev/null || true)
# Validate that we are inside a git repository
if [[ -z "$ROOT_DIR" ]]; then
  echo "Error: This script must be run inside a Git repository."
  exit 1
fi

# Change directory to the root of the project
# This ensures .venv is always created in the right place
cd "$ROOT_DIR"

# Check if the .venv directory already exists
if [ ! -d ".venv" ]; then
  echo "+ Creating virtual environment..."
  uv venv
else
  echo ": Virtual environment already exists"
fi

# Install dependencies using the lockfile
echo ": Sync dependencies from uv.lock..."
uv run uv sync --frozen --quiet

# Install git hooks
echo "+ Installing git hooks..."
uv run pre-commit install
uv run pre-commit install --hook-type pre-push

# Install the current project in editable mode
echo "+ Installing project in editable mode..."
uv run uv pip install -e . --quiet

echo "--- DEV setup completed successfully ---"
