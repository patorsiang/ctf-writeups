#!/bin/sh
set -e
HOST="http://34.158.35.47"
KEY="hearth-porch-6d13"
JAR="$(dirname "$0")/cookies_probe2.txt"
rm -f "$JAR"

try() {
  echo "-- $1 --"
  shift
  curl -sS -m 10 -b "$JAR" -c "$JAR" -o - -w '\n[%{http_code}]\n' "$@" | tail -c 600
  echo
}

try "GET hearth/old with key" -H "X-Hearth-Key: $KEY" "$HOST/api/v1/hearth/old"
try "GET hearth/open?gate=keeper" -H "X-Hearth-Key: $KEY" "$HOST/api/v1/hearth/open?gate=keeper"
try "GET hearth/open with X-Hearth-Gate: keeper" -H "X-Hearth-Key: $KEY" -H "X-Hearth-Gate: keeper" "$HOST/api/v1/hearth/open"
try "GET hearth/open/keeper" -H "X-Hearth-Key: $KEY" "$HOST/api/v1/hearth/open/keeper"
try "GET vault/board?gate=keeper" "$HOST/vault/board?gate=keeper"
try "GET /api/v1/hearth/keeper" -H "X-Hearth-Key: $KEY" "$HOST/api/v1/hearth/keeper"
try "GET /vault/keeper" "$HOST/vault/keeper"
try "GET /vault/slate" "$HOST/vault/slate"
try "GET /keeper/slate" "$HOST/keeper/slate"
