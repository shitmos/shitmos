#!/bin/bash
export OSMOSISD_KEYRING_BACKEND=file

# Transaction is saved here
TRANSACTIONS_DIR="../data/transactions"

# If you are starting fresh, this makes directory if directory not there
mkdir -p $TRANSACTIONS_DIR

# Run get_wallet_balances.py first
echo "Fetching initial wallet balances..."
python get_wallet_balances.py sez --keyring-backend file

# Run print_shitdribble.py to display distributions
echo "Displaying distribution details..."
python print_shitdribble.py

# Transaction generation
PYTHON_SCRIPT_PATH="./generate_shitdribble.py"
FROM_ADDRESS=$(osmosisd keys show sez -a --keyring-backend file)

# Run the Python script and capture the output
echo "Generating transaction data..."
OUTPUT=$(python $PYTHON_SCRIPT_PATH --denom CRAZYHORSE --amount 1 --from-address "$FROM_ADDRESS")

# Print the entire output to debug
echo "Full output from Python script:"
echo "$OUTPUT"

# Extract the last line, assuming it's the JSON file path
JSON_FILE=$(echo "$OUTPUT" | tail -n 1)

# Validate JSON file existence
if [ ! -f "$JSON_FILE" ]; then
    echo "JSON file not found: $JSON_FILE"
    exit 1
fi

echo "Generated JSON file: $JSON_FILE"

# Parameters for the transaction
# Use the correct key name
KEY_NAME="sez"
CHAIN_ID="osmosis-1"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Confirm if want to sign, and then sign
read -p "Are you sure you want to sign the transaction? (y/n) " confirm_sign
if [[ "$confirm_sign" == "y" || "$confirm_sign" == "Y" ]]; then
    SIGN_OUTPUT="${TRANSACTIONS_DIR}/signed_tx_${TIMESTAMP}.json"
    echo "Signing the transaction using file: $JSON_FILE"

    # Here is the actual use of the osmosisd CLI
    osmosisd tx sign "$JSON_FILE" --from "$KEY_NAME" --chain-id "$CHAIN_ID" --keyring-backend file --output-document "$SIGN_OUTPUT"

    # Check if the signing was successful
    if [ $? -ne 0 ]; then
        echo "Error signing the transaction"
        exit 1
    fi
else
    echo "Transaction signing cancelled."
    exit 0
fi

# Confirm if want to broadcast, and then broadcast
read -p "You will broadcast this transaction, are you sure you want to proceed? (y/n) " confirm_broadcast
if [[ "$confirm_broadcast" == "y" || "$confirm_broadcast" == "Y" ]]; then
    
    echo "Broadcasting the signed transaction..."
    osmosisd tx broadcast "$SIGN_OUTPUT"

    # Check if broadcast worked
    if [ $? -ne 0 ]; then
        echo "Error broadcasting the transaction"
        exit 1
    fi
else
    echo "Transaction broadcasting cancelled."
    exit 0
fi

# After 5 second countdown, run get_wallet_balances.py one last time
echo "Waiting for 5 seconds before fetching final wallet balances..."
sleep 5

echo "Fetching final wallet balances..."
python get_wallet_balances.py sez --keyring-backend file
