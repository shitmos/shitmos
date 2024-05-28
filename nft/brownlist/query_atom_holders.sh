# Set your node endpoint
NODE_ENDPOINT="https://cosmoshub-node-endpoint.com"

# Function to convert ATOM balance from uatom
convert_uatom_to_atom() {
  echo "scale=6; $1 / 1000000" | bc
}

# Get all accounts
curl -s "$NODE_ENDPOINT/cosmos/auth/v1beta1/accounts" | jq -r '.accounts[].address' | while read -r address; do
  # Get account balance
  balance=$(curl -s "$NODE_ENDPOINT/cosmos/bank/v1beta1/balances/$address" | jq -r '.balances[] | select(.denom == "uatom") | .amount')
  atom_balance=$(convert_uatom_to_atom $balance)

  # Check if balance is greater than 22 ATOM
  if (( $(echo "$atom_balance > 22" | bc -l) )); then
    echo "Address: $address, Balance: $atom_balance ATOM"
  fi
done
