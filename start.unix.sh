#!/usr/bin/env bash
# Start the PHREEQC Workbench backend + open the frontend in a browser.
#
# This is the root-directory launcher (equivalent to workbench/start.unix.sh
# but invoked directly from the repo root).
#
# Tested on:
#     - Linux   (Ubuntu 22.04+, Fedora 39+)     with xdg-open
#     - macOS   (12 Monterey, 13 Ventura, 14 Sonoma)  with `open`
#     - Git Bash on Windows                    with `start`
#
# Usage:
#     ./start.unix.sh                  # default port 8765
#     ./start.unix.sh 8780             # custom port
#     PORT=8780 ./start.unix.sh        # via env var

set -euo pipefail

PORT="${1:-${PORT:-8765}}"
HOST="${HOST:-127.0.0.1}"
ROOT="$(cd "$(dirname "$0")" && pwd)"

cd "$ROOT"

# Optional UTF-8 for Chinese Windows terminals.
export PYTHONIOENCODING="${PYTHONIOENCODING:-utf-8}"

# Use the existing virtualenv if it exists, otherwise fall back to the
# interpreter on PATH.  This keeps the workbench zero-dep: it only
# needs the four stdlib modules it imports (no FastAPI, no uvicorn).
PY="${PYTHON:-}"
if [ -z "$PY" ] && [ -x "$ROOT/.venv/Scripts/python.exe" ]; then
    PY="$ROOT/.venv/Scripts/python.exe"
elif [ -z "$PY" ] && [ -x "$ROOT/.venv/bin/python" ]; then
    PY="$ROOT/.venv/bin/python"
elif [ -z "$PY" ]; then
    PY="$(command -v python3 || command -v python)"
fi

if [ -z "$PY" ]; then
    echo "[workbench] ERROR: no Python interpreter found." >&2
    exit 1
fi

echo "[workbench] Python:    $PY"
echo "[workbench] Project:   $ROOT"
echo "[workbench] Frontend:  http://$HOST:$PORT/"

# Best-effort browser launch (non-fatal if it fails).
URL="http://$HOST:$PORT/"
if command -v xdg-open >/dev/null 2>&1; then
    (xdg-open "$URL" >/dev/null 2>&1 || true) &
elif command -v open >/dev/null 2>&1; then
    (open "$URL" >/dev/null 2>&1 || true) &
elif command -v start >/dev/null 2>&1; then
    (start "$URL" >/dev/null 2>&1 || true) &
fi

# Start the server in the foreground so Ctrl-C works.
exec "$PY" "$ROOT/workbench/backend/app.py" --host "$HOST" --port "$PORT"