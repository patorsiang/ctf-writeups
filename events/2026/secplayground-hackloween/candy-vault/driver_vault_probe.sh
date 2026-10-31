#!/bin/sh
HOST="http://34.158.35.47"
TOKEN="cturnG_IkB0DFsKXIZPWlQvW-OUzlgIfDXDoSv9lBEA"

try() {
  printf '%-40s ' "$1"
  curl -sS -m 10 -H "Authorization: Bearer $TOKEN" -o /tmp/vb_$$.out -w '%{http_code}\n' "$HOST$1"
  cat /tmp/vb_$$.out; echo; rm -f /tmp/vb_$$.out
}

for p in /api/v1/driver/manifest /api/v1/driver/vault /api/v1/driver/board /api/v1/driver/route \
         /api/v1/vault /api/v1/vault/board /api/v1/vault/manifest /api/v1/driver/deliveries \
         /api/v1/driver/stops /api/v1/driver/keeper /api/v1/keeper /api/v1/keeper/slate \
         /api/v1/vault/keeper; do
  try "$p"
done
