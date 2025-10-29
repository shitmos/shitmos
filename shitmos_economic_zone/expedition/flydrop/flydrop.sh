#!/usr/bin/env bash
set -euo pipefail

# ── DEBUG TOGGLE ──────────────────────────────────────────────────────────────
# export DEBUG=1 to enable bash tracing + extra prints
DEBUG="${DEBUG:-0}"

# ── CONFIG ────────────────────────────────────────────────────────────────────
KEY_NAME="flydrop"                          # key name in osmosisd keyring
KEYRING="file"                              # file|os|test
CHAIN_ID="osmosis-1"
NODE="https://rpc.osmosis.zone:443"
GAS_PRICES="0.025uosmo"
GAS_ADJUSTMENT="1.2"

DENOM="factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/crazyhorse"                               # token you’re sending
AMOUNT_PER_ADDRESS="100"                    # e.g., 100 uosmo per recipient
CHUNK=200                                   # recipients per tx (one prompt per chunk)
MEMO="flydrop"

INPUT_FILE="addresses.txt"                  # one bech32 per line (stars1… or osmo1…)

# Optional sweep (disabled by default)
SWEEP_REMAINDER="false"
SWEEP_ADDRESS="osmo1gz7t9aaqwnmdhn5umm03rqqxd9spkjx3he4xkz"
SWEEP_FEE_AMOUNT="5000"
SWEEP_FEE_DENOM="uosmo"

# ── PYTHON + LAYOUT ───────────────────────────────────────────────────────────
PY_BIN="$(command -v python3.11 || command -v python3)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GEN_PY="$SCRIPT_DIR/generate_flydrop.py"

# Propagate keyring backend to child procs
export OSMOSISD_KEYRING_BACKEND="$KEYRING"

mkdir -p "$SCRIPT_DIR/flydrops"
next_run() { local n=1; while [[ -d "$SCRIPT_DIR/flydrops/flydrop_$(printf "%04d" "$n")" ]]; do n=$((n+1)); done; printf "%04d" "$n"; }
RUN_NUM="$(next_run)"
RUN_DIR="$SCRIPT_DIR/flydrops/flydrop_${RUN_NUM}"
TX_DIR="$RUN_DIR/transactions"
BAL_DIR="$RUN_DIR/balances"
LOG_DIR="$RUN_DIR/logs"
mkdir -p "$TX_DIR" "$BAL_DIR" "$LOG_DIR"

if [[ "$DEBUG" == "1" ]]; then
  echo "=== DEBUG MODE ON ==="
  set -x
  echo "whoami: $(whoami)"
  echo "pwd: $(pwd)"
  echo "which osmosisd: $(command -v osmosisd || true)"
  echo "osmosisd version: $(osmosisd version || true)"
  echo "which python: $PY_BIN"
  echo "CHAIN_ID=$CHAIN_ID"
  echo "NODE=$NODE"
  echo "KEY_NAME=$KEY_NAME"
  echo "KEYRING=$KEYRING (OSMOSISD_KEYRING_BACKEND=$OSMOSISD_KEYRING_BACKEND)"
fi

echo "=================================================================="
echo "🚀 FLYDROP — run: flydrop_${RUN_NUM}"
echo "node:          $NODE"
echo "chain-id:      $CHAIN_ID"
echo "key/keyring:   ${KEY_NAME}/${KEYRING}"
echo "denom/amount:  ${AMOUNT_PER_ADDRESS}${DENOM}"
echo "chunk size:    $CHUNK"
echo "input file:    $INPUT_FILE"
echo "snapshot dir:  $RUN_DIR"
echo "=================================================================="
echo

# ── PRECHECKS ─────────────────────────────────────────────────────────────────
command -v osmosisd >/dev/null || { echo "❌ osmosisd not found on PATH"; exit 1; }
command -v "$PY_BIN"  >/dev/null || { echo "❌ python not found"; exit 1; }
[[ -f "$INPUT_FILE" ]] || { echo "❌ missing $INPUT_FILE"; exit 1; }

# keys inventory (helps diagnose wrong keyring)
{
  echo "── keys (file backend)";  osmosisd keys list --keyring-backend file || true
  echo "── keys (os backend)";    osmosisd keys list --keyring-backend os   || true
} | tee "$LOG_DIR/keys_inventory.txt" >/dev/null

# verify key exists in chosen keyring
if ! osmosisd keys list --keyring-backend "$KEYRING" | grep -q "name: ${KEY_NAME}"; then
  echo "❌ key '${KEY_NAME}' not found in keyring '${KEYRING}'."
  echo "   add it: osmosisd keys add ${KEY_NAME} --recover --keyring-backend ${KEYRING}"
  exit 1
fi

echo "🔑 resolving sender address (you may be prompted for passphrase)…"
FROM_ADDRESS="$(osmosisd keys show "$KEY_NAME" -a --keyring-backend "$KEYRING")"
echo "from address: $FROM_ADDRESS"
echo

# snapshot inputs
cp "$INPUT_FILE" "$RUN_DIR/addresses_input.txt"

# ── KEYRING SMOKE TEST (prove prompts work; no broadcast) ────────────────────
echo "🫧 keyring smoke test (generate-only tiny tx; no broadcast)…"
TEST_TMP="$RUN_DIR/keyring_smoketest.json"
if osmosisd tx bank send \
  "$KEY_NAME" "$FROM_ADDRESS" "1$DENOM" \
  --chain-id "$CHAIN_ID" --node "$NODE" \
  --gas auto --gas-prices "$GAS_PRICES" --gas-adjustment "$GAS_ADJUSTMENT" \
  --keyring-backend "$KEYRING" --generate-only --output json > "$TEST_TMP"; then
  echo "   ✓ smoke test OK → $TEST_TMP"
else
  echo "   ⚠️ smoke test FAILED. Inspect params/backends."
fi
echo

# ── INITIAL BALANCES ──────────────────────────────────────────────────────────
echo "⏳ querying initial balances…"
osmosisd q bank balances "$FROM_ADDRESS" --node "$NODE" --output json \
  | tee "$BAL_DIR/initial.json" >/dev/null || echo "⚠️  failed to fetch initial balances"
echo

# ── GENERATE UNSIGNED TX JSONS ────────────────────────────────────────────────
TOTAL_RECIPS=$(grep -vc '^\s*$' "$INPUT_FILE" || true)
echo "🛠  generating unsigned transactions…"
echo "    recipients (raw lines): $TOTAL_RECIPS"
echo

GEN_OUTPUT="$("$PY_BIN" "$GEN_PY" \
  --input "$INPUT_FILE" \
  --denom "$DENOM" \
  --amount "$AMOUNT_PER_ADDRESS" \
  --from-key "$KEY_NAME" \
  --from-address "$FROM_ADDRESS" \
  --chunk "$CHUNK" \
  --memo "$MEMO" \
  --chain-id "$CHAIN_ID" \
  --node "$NODE" \
  --gas-prices "$GAS_PRICES" \
  --gas-adjustment "$GAS_ADJUSTMENT" \
  --keyring-backend "$KEYRING" \
  --output-dir "$TX_DIR" \
  --verbose \
  )"

echo "$GEN_OUTPUT" | tee "$LOG_DIR/generate.log" >/dev/null

TX_FILES=$(echo "$GEN_OUTPUT" | grep -oE 'saved: .*\.json' | awk '{print $2}')
if [[ -z "${TX_FILES:-}" ]]; then
  echo "❌ no tx JSONs generated (see $LOG_DIR/generate.log and $TX_DIR/_debug/*)"; exit 1
fi

TX_COUNT=$(echo "$TX_FILES" | wc -w | tr -d ' ')
echo
echo "📦 unsigned transactions created: $TX_COUNT"
echo "    folder: $TX_DIR"
echo

# ── SIGN + BROADCAST ──────────────────────────────────────────────────────────
i=0
for JSON_FILE in $TX_FILES; do
  i=$((i+1))
  echo "──────────────────────────────────────────────────────────────────"
  echo "→ [$i/$TX_COUNT] tx file: $JSON_FILE"
  SIGNED_FILE="${JSON_FILE%.json}_signed.json"

  read -p "Sign this tx with key '${KEY_NAME}'? (y/n) " ans
  [[ "$ans" =~ ^[Yy]$ ]] || { echo "skip"; continue; }

  echo "✍️  signing… (keyring: $KEYRING, passphrase will prompt in terminal)"
  if ! osmosisd tx sign "$JSON_FILE" \
    --from "$KEY_NAME" \
    --chain-id "$CHAIN_ID" \
    --keyring-backend "$KEYRING" \
    --output-document "$SIGNED_FILE"; then
      echo "❌ signing failed for $JSON_FILE"
      continue
  fi

  echo "📡 broadcast? (y/n)"
  read ans2
  if [[ "$ans2" =~ ^[Yy]$ ]]; then
    echo "…broadcasting to $NODE"
    osmosisd tx broadcast "$SIGNED_FILE" --node "$NODE" \
      | tee "${SIGNED_FILE%.json}_broadcast.txt"
  else
    echo "skipped broadcast"
  fi
done
echo "──────────────────────────────────────────────────────────────────"

# ── FINAL BALANCES ────────────────────────────────────────────────────────────
echo "⏳ querying final balances…"
osmosisd q bank balances "$FROM_ADDRESS" --node "$NODE" --output json \
  | tee "$BAL_DIR/final.json" >/dev/null || echo "⚠️  failed to fetch final balances"

if [[ "$SWEEP_REMAINDER" == "true" ]]; then
  echo "🔁 sweeping remainder to ${SWEEP_ADDRESS} (fee ${SWEEP_FEE_AMOUNT}${SWEEP_FEE_DENOM})"
  # Example (disabled):
  # osmosisd tx bank send "$FROM_ADDRESS" "$SWEEP_ADDRESS" "1${DENOM}" \
  #   --chain-id "$CHAIN_ID" --keyring-backend "$KEYRING" \
  #   --fees "${SWEEP_FEE_AMOUNT}${SWEEP_FEE_DENOM}" --node "$NODE"
fi

echo
echo "✅ done → $RUN_DIR"
