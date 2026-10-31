#!/bin/sh
HOST="http://34.158.35.47"
KEY="hearth-porch-6d13"
TOKEN="cturnG_IkB0DFsKXIZPWlQvW-OUzlgIfDXDoSv9lBEA"
JAR="$(dirname "$0")/cookies3.txt"
rm -f "$JAR"

echo "== open session, keep cookie =="
OPEN=$(curl -sS -m 15 -c "$JAR" -H "X-Hearth-Key: $KEY" "$HOST/api/v1/hearth/open")
echo "$OPEN"
NONCE=$(echo "$OPEN" | python3 -c "import sys,json; print(json.load(sys.stdin)['nonce'])")
echo "nonce=$NONCE"

T1=$(python3 -c "import hashlib; print(hashlib.sha256(('$NONCE:$TOKEN').encode()).hexdigest()[:16])")
T2=$(python3 -c "import hashlib; print(hashlib.sha256(('$TOKEN:$NONCE').encode()).hexdigest()[:16])")
echo "turn(nonce,token)=$T1"
echo "turn(token,nonce)=$T2"

try() {
  echo "-- $1 --"; shift
  curl -sS -m 10 -b "$JAR" -o - -w '\n[%{http_code}]\n' "$@" | tail -c 500
  echo
}

try "hearth/open with X-Hearth-Key=turn(nonce,token), same cookie" -H "X-Hearth-Key: $T1" "$HOST/api/v1/hearth/open"
try "hearth/open with X-Hearth-Key=turn(token,nonce), same cookie" -H "X-Hearth-Key: $T2" "$HOST/api/v1/hearth/open"
try "vault/board with X-Hearth-Key=turn(nonce,token)" -H "X-Hearth-Key: $T1" "$HOST/vault/board"
try "vault/board?key=turn(nonce,token)" "$HOST/vault/board?key=$T1"
try "vault/board with Authorization Bearer token AND cookie" -H "Authorization: Bearer $TOKEN" "$HOST/vault/board"
try "hearth/open with Authorization Bearer token, X-Hearth-Key base" -H "X-Hearth-Key: $KEY" -H "Authorization: Bearer $TOKEN" "$HOST/api/v1/hearth/open"
