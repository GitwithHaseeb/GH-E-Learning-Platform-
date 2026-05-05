#!/usr/bin/env bash
set -euo pipefail
# PostgreSQL dump — usage: DB_URL=postgres://user:pass@host:5432/db ./backup.sh
OUT="${1:-backup.sql}"
if [[ -n "${DB_URL:-}" ]]; then
  pg_dump "$DB_URL" > "$OUT"
else
  echo "Set DB_URL (postgres connection string) first."
  exit 1
fi
echo "Wrote $OUT"
