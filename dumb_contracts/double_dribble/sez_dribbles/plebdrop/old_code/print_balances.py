import subprocess
import json
import pandas as pd

# Addresses
osmosis_addr = "osmo1r6f5tfxdx2pw5p94f2v5n96xd4nglz5q30mczj"
stargaze_addr = "stars1r6f5tfxdx2pw5p94f2v5n96xd4nglz5qdgl4l3"

# Token mapping file
token_mapping_file = "token_mapping.csv"

def load_token_mapping(file_path):
    """
    Load the token mapping from a CSV file into a dictionary.
    """
    try:
        df = pd.read_csv(file_path)
        mapping = {row['denom']: row['name'] if pd.notna(row['name']) else row['denom'] for _, row in df.iterrows()}
        return mapping
    except Exception as e:
        print(f"Failed to load token mapping file: {e}")
        return {}

def run_command(command):
    """
    Run a shell command and return its output, capturing both stdout and stderr.
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stdout.strip():
            return result.stdout.strip()
        elif result.stderr.strip():
            return result.stderr.strip()
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}\nSTDERR: {e.stderr}\nSTDOUT: {e.stdout}")
        return None

def query_balances(cli_tool_path, address):
    """
    Query balances for a given CLI tool and address.
    """
    command = [cli_tool_path, "query", "bank", "balances", address, "-o", "json"]
    print(f"Running command: {' '.join(command)}")
    output = run_command(command)

    if not output:
        print(f"\nCommand returned no output for {cli_tool_path}. Check configuration.")
        return None

    try:
        return json.loads(output).get("balances", [])
    except json.JSONDecodeError as e:
        print(f"\nFailed to decode JSON from {cli_tool_path}: {e}")
        return None

def process_balances(balances, token_mapping):
    """
    Convert balances into a DataFrame, replace denoms with token names,
    and format the amounts with two decimals and commas.
    """
    if not balances:
        return None
    df = pd.DataFrame(balances)
    df.columns = ["Denom", "Amount"]
    df["Denom"] = df["Denom"].apply(lambda x: token_mapping.get(x, x))  # Replace with token name or default to denom
    df["Amount"] = df["Amount"].astype(int) / 1_000_000  # Convert micro-units to units
    df["Amount"] = df["Amount"].apply(lambda x: f"{x:,.2f}")  # Format with commas and two decimals
    return df

def main():
    # Full paths to CLI tools
    osmosisd_path = "/usr/local/bin/osmosisd"
    starsd_path = "/home/flarnrules/go/bin/starsd"

    # Load token mapping
    token_mapping = load_token_mapping(token_mapping_file)

    # Query Osmosis balances
    osmosis_balances = query_balances(osmosisd_path, osmosis_addr)
    if osmosis_balances is not None:
        osmosis_table = process_balances(osmosis_balances, token_mapping)
        if osmosis_table is not None:
            print("\nOsmosis Balances Table:")
            print(osmosis_table)
        else:
            print("\nNo Osmosis balances found.")

    # Query Stargaze balances
    stargaze_balances = query_balances(starsd_path, stargaze_addr)
    if stargaze_balances is not None:
        stargaze_table = process_balances(stargaze_balances, token_mapping)
        if stargaze_table is not None:
            print("\nStargaze Balances Table:")
            print(stargaze_table)
        else:
            print("\nNo Stargaze balances found.")

if __name__ == "__main__":
    main()
