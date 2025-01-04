#!/bin/bash

# Set paths to Python scripts
PRINT_BALANCES_SCRIPT="print_balances.py"
GENERATE_TRANSACTIONS_SCRIPT="generate_transactions.py"
TRANSACTIONS_DIR="transactions"

# Ensure necessary directories exist
mkdir -p $TRANSACTIONS_DIR

# Step 1: Print starting balances
echo "Step 1: Fetching starting balances..."
python3 $PRINT_BALANCES_SCRIPT > starting_balances.txt
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to fetch starting balances."
    exit 1
fi
echo "Starting balances saved to starting_balances.txt."

# Step 2: Generate transactions
echo "Step 2: Generating transactions..."
python3 $GENERATE_TRANSACTIONS_SCRIPT
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to generate transactions."
    exit 1
fi
echo "Transactions generated and saved in the $TRANSACTIONS_DIR directory."

# Step 3: Display summary of transactions
echo "Step 3: Summary of transactions to be broadcast:"
find $TRANSACTIONS_DIR -type f -name "*.json" | sort | xargs cat | jq '.body.messages[] | {to_address: .to_address, amount: .amount}' > transaction_summary.json
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to generate transaction summary."
    exit 1
fi
cat transaction_summary.json

# Confirm before broadcasting
read -p "Do you want to proceed with broadcasting these transactions? (y/n): " confirm
if [[ $confirm != "y" ]]; then
    echo "Broadcasting canceled. Exiting."
    exit 0
fi

# Step 4: Broadcast transactions
echo "Step 4: Broadcasting transactions..."
for tx_file in $TRANSACTIONS_DIR/*.json; do
    echo "Broadcasting transaction: $tx_file"
    blockchain=$(echo $tx_file | grep -oE '(osmosis|stargaze)')
    if [[ $blockchain == "osmosis" ]]; then
        cli_tool="osmosisd"
    elif [[ $blockchain == "stargaze" ]]; then
        cli_tool="starsd"
    else
        echo "Error: Unknown blockchain in $tx_file."
        continue
    fi

    $cli_tool tx broadcast $tx_file --yes --keyring-backend file
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to broadcast $tx_file."
        continue
    fi
    echo "Transaction $tx_file broadcast successfully."
done

# Step 5: Print ending balances
echo "Step 5: Fetching ending balances..."
python3 $PRINT_BALANCES_SCRIPT > ending_balances.txt
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to fetch ending balances."
    exit 1
fi
echo "Ending balances saved to ending_balances.txt."

# Step 6: Calculate differences in balances
echo "Step 6: Calculating balance differences..."
python3 - <<EOF
import pandas as pd

# Load starting and ending balances
start = pd.read_csv('starting_balances.txt', sep="\t", header=None, names=["Denom", "Amount"])
end = pd.read_csv('ending_balances.txt', sep="\t", header=None, names=["Denom", "Amount"])

# Merge and calculate differences
merged = pd.merge(start, end, on="Denom", suffixes=("_start", "_end"))
merged["Difference"] = merged["Amount_end"] - merged["Amount_start"]
print(merged[["Denom", "Amount_start", "Amount_end", "Difference"]])
EOF

echo "Airdrop completed."
