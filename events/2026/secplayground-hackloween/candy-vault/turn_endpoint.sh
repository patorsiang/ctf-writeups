#!/bin/sh
HOST="http://34.158.35.47"
KEY="hearth-porch-6d13"
JAR="$(dirname "$0")/cookies4.txt"
rm -f "$JAR"

echo "== open fresh session =="
OPEN=$(curl -sS -m 15 -c "$JAR" -H "X-Hearth-Key: $KEY" "$HOST/api/v1/hearth/open")
echo "$OPEN"
NONCE=$(echo "$OPEN" | python3 -c "import sys,json; print(json.load(sys.stdin)['nonce'])")
TURN=$(python3 -c "import hashlib; print(hashlib.sha256(('$NONCE:$KEY').encode()).hexdigest()[:16])")
echo "nonce=$NONCE turn=$TURN"

echo "== OPTIONS /api/v1/hearth/turn =="
curl -sS -m 10 -i -X OPTIONS "$HOST/api/v1/hearth/turn" | head -10

echo "== POST /api/v1/hearth/turn with turn value, json body =="
curl -sS -m 10 -b "$JAR" -i -X POST -H "Content-Type: application/json" \
  -d "{\"turn\":\"$TURN\"}" "$HOST/api/v1/hearth/turn"

echo
echo "== POST /api/v1/hearth/turn with turn as form field =="
curl -sS -m 10 -b "$JAR" -i -X POST -d "turn=$TURN" "$HOST/api/v1/hearth/turn"

echo
echo "== POST /api/v1/hearth/turn with X-Hearth-Key header (base), turn in body =="
curl -sS -m 10 -b "$JAR" -i -X POST -H "X-Hearth-Key: $KEY" -H "Content-Type: application/json" \
  -d "{\"turn\":\"$TURN\",\"nonce\":\"$NONCE\"}" "$HOST/api/v1/hearth/turn"
