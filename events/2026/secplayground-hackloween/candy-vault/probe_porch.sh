#!/bin/sh
# Exploratory probe for the Candy Vault "porch" gate.
# Opens a fresh hearth session, computes Scenario.turn(nonce, key) both ways
# (SHA256(a+":"+b)[:16], matching the APK's Scenario.turn), then tries several
# plausible places to submit it, keeping the matching session cookie throughout.
set -e
HOST="http://34.158.35.47"
KEY="hearth-porch-6d13"
JAR="$(dirname "$0")/cookies_probe.txt"
rm -f "$JAR"

echo "== open session =="
OPEN=$(curl -sS -m 15 -c "$JAR" -H "X-Hearth-Key: $KEY" "$HOST/api/v1/hearth/open")
echo "$OPEN"
NONCE=$(echo "$OPEN" | python3 -c "import sys,json; print(json.load(sys.stdin)['nonce'])")
echo "nonce=$NONCE"

TURN_NK=$(python3 -c "
import hashlib
print(hashlib.sha256(('$NONCE:$KEY').encode()).hexdigest()[:16])
")
TURN_KN=$(python3 -c "
import hashlib
print(hashlib.sha256(('$KEY:$NONCE').encode()).hexdigest()[:16])
")
echo "turn(nonce,key)=$TURN_NK"
echo "turn(key,nonce)=$TURN_KN"

try() {
  echo "-- $1 --"
  shift
  curl -sS -m 10 -b "$JAR" -o - -w '\n[%{http_code}]\n' "$@"
  echo
}

try "GET /vault/board with cookie only" "$HOST/vault/board"
try "GET hearth/open with X-Hearth-Turn (nonce,key)" -H "X-Hearth-Key: $KEY" -H "X-Hearth-Turn: $TURN_NK" "$HOST/api/v1/hearth/open"
try "GET hearth/open with X-Hearth-Turn (key,nonce)" -H "X-Hearth-Key: $KEY" -H "X-Hearth-Turn: $TURN_KN" "$HOST/api/v1/hearth/open"
try "GET vault/board?turn=(nonce,key)" "$HOST/vault/board?turn=$TURN_NK"
try "GET vault/board?turn=(key,nonce)" "$HOST/vault/board?turn=$TURN_KN"
try "GET /api/v1/hearth/turn?turn=(nonce,key)" "$HOST/api/v1/hearth/turn?turn=$TURN_NK"
try "GET /api/v1/hearth/porch?turn=(nonce,key)" "$HOST/api/v1/hearth/porch?turn=$TURN_NK"
try "GET /api/v1/hearth/porch?key=(nonce,key)" "$HOST/api/v1/hearth/porch?key=$TURN_NK"
try "GET vault/board with X-Hearth-Turn header (nonce,key)" -H "X-Hearth-Turn: $TURN_NK" "$HOST/vault/board"
