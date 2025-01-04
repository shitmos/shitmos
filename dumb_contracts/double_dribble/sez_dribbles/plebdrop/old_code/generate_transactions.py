import os
import json
import config
import pandas as pd
import datetime
import bech32


def convert_address(stargaze_address, target_prefix="osmo"):
    """
    Convert a Stargaze address to an Osmosis address.
    """
    try:
        hrp, data = bech32.bech32_decode(stargaze_address)
        if data is None:
            print(f"Invalid Stargaze address: {stargaze_address}")
            return None
        return bech32.bech32_encode(target_prefix, data)
    except Exception as e:
        print(f"Error converting address: {e}")
        return None


def resolve_path(path):
    """Resolve the absolute path relative to the script directory."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(script_dir, path))


def load_csv(file_path, single_column=False):
    """
    Load the CSV file and handle single-column CSVs if needed.
    """
    try:
        if single_column:
            return pd.read_csv(file_path, header=0, names=["address"])
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV file '{file_path}': {e}")
        exit(1)


def get_denom_from_token_mapping(token_name, token_mapping_file):
    """
    Retrieve the full denom for a token name from the token mapping file.
    """
    try:
        token_mapping = pd.read_csv(token_mapping_file)
        row = token_mapping[token_mapping["symbol"].str.upper() == token_name.upper()]
        if not row.empty:
            return row.iloc[0]["denom"]
        else:
            print(f"Token {token_name} not found in token_mapping.csv.")
            return None
    except Exception as e:
        print(f"Error reading token_mapping.csv: {e}")
        return None


def create_transaction(messages, fee_denom, fee_amount, gas_limit):
    """
    Create a Cosmos SDK transaction JSON object.
    """
    return {
        "msg": messages,
        "fee": {
            "amount": [{"denom": fee_denom, "amount": str(fee_amount)}],
            "gas": str(gas_limit),
        },
        "signatures": None,
        "memo": "",
    }


def save_transaction(transaction, index, transactions_dir, blockchain):
    """
    Save the transaction JSON to a file with blockchain metadata.
    """
    os.makedirs(transactions_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"{blockchain}_transaction_{timestamp}_{index:04d}.json"
    file_path = os.path.join(transactions_dir, file_name)

    with open(file_path, "w") as f:
        json.dump({"blockchain": blockchain, "transaction": transaction}, f, indent=4)

    print(f"Transaction saved: {file_path}")


def handle_naughty_list(from_address, blockchain, transactions_dir, token_mapping_file):
    """
    Process the naughty list with fixed allocations per wallet.
    """
    token_mapping = pd.read_csv(token_mapping_file)
    blockchain_settings = config.get_blockchain_settings(blockchain)
    fee_denom = blockchain_settings["fee_denom"]
    fee_amount = blockchain_settings["fee_amount"]
    gas_limit = blockchain_settings["gas_limit"]

    token_name = config.NAUGHTY_LIST_TOKEN
    denom = get_denom_from_token_mapping(token_name, token_mapping_file)
    if not denom:
        print(f"Error: Denom for token {token_name} not found.")
        return

    df = load_csv(config.NAUGHTY_LIST_CSV_FILE, single_column=True)

    messages = []
    transactions = []

    for idx, row in df.iterrows():
        stargaze_address = row["address"].strip()
        osmosis_address = convert_address(stargaze_address, "osmo")
        if not osmosis_address:
            print(f"Skipping invalid address: {stargaze_address}")
            continue

        amount_in_micro_units = int(config.NAUGHTY_LIST_AMOUNT * config.CONVERSION_RATE)
        messages.append({
            "@type": "/cosmos.bank.v1beta1.MsgSend",
            "from_address": from_address,
            "to_address": osmosis_address,
            "amount": [{"denom": denom, "amount": str(amount_in_micro_units)}],
        })

        if len(messages) >= config.MAX_MESSAGES_PER_TX:
            transactions.append(create_transaction(messages, fee_denom, fee_amount, gas_limit))
            messages = []

    if messages:
        transactions.append(create_transaction(messages, fee_denom, fee_amount, gas_limit))

    for idx, tx in enumerate(transactions):
        save_transaction(tx, idx, transactions_dir, blockchain)

    print(f"Generated {len(transactions)} transactions for naughty list.")


def main():
    from_address = config.get_sender_address("osmosis")  # Dynamically fetch sender address
    blockchain = input("Enter the blockchain (osmosis/stargaze): ").strip().lower()
    list_type = input("Which list to process? (naughty/nice): ").strip().lower()
    transactions_dir = resolve_path("transactions")
    token_mapping_file = resolve_path("token_mapping.csv")

    if list_type == "naughty":
        print("Processing naughty list...")
        handle_naughty_list(from_address, blockchain, transactions_dir, token_mapping_file)
    else:
        print("Nice list processing is not implemented yet.")


if __name__ == "__main__":
    main()