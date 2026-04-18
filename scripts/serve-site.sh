#!/usr/bin/env bash
# Serve site/ over HTTP so fetch() (e.g. raw_data.json) works. Default: http://127.0.0.1:8080/
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE="$REPO_ROOT/site"
PORT="${PORT:-8080}"
echo "Serving: $SITE"
echo "  Home:     http://127.0.0.1:$PORT/"
echo "  Aphorism: http://127.0.0.1:$PORT/irregulars/aphorism.html"
echo "Press Ctrl+C to stop."
exec python3 -m http.server "$PORT" --bind 127.0.0.1 -d "$SITE"
