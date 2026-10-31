#!/bin/sh
set -e
HOST="http://34.158.35.47"
TOKEN="cturnG_IkB0DFsKXIZPWlQvW-OUzlgIfDXDoSv9lBEA"

echo "== profile =="
curl -sS -m 15 -i -H "Authorization: Bearer $TOKEN" "$HOST/api/v1/driver/profile"
echo
echo "== vault/board with bearer =="
curl -sS -m 15 -i -H "Authorization: Bearer $TOKEN" "$HOST/vault/board"
