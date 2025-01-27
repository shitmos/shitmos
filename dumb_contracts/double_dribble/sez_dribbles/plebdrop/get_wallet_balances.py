#!/usr/bin/env python3
import argparse
import json
import subprocess
import config

def convert_micro_to_unit(micro_amount):
    return micro_amount / config.CONVERSION_RATE

def format_balance(amount):
    return f"{amount:,.2f}"

def get_balances(address):
    """Retrieve balances for the given hardcoded address."""
    try:
        # Query balances
        balances_raw = subprocess.check_output(
            ["starsd", "query", "bank", "balances", address, "-o", "json"],
            stderr=subprocess.STDOUT
        ).decode("utf-8")
        balances_json = json.loads(balances_raw)
        balances = balances_json.get("balances", [])

        # Convert balances to standard units
        standard_balances = {}
        for balance in balances:
            denom = balance.get("denom")
            amount_micro = int(balance.get("amount"))
            amount_standard = convert_micro_to_unit(amount_micro)
            # Map full denom to common name
            common_name = config.TOKEN_NAME_MAPPING.get(denom, denom)
            standard_balances[common_name] = amount_standard

        return standard_balances
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving balances: {e.output.decode('utf-8')}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

def print_balances(standard_balances):
    """Print balances in a formatted table."""
    if standard_balances:
        max_denom_length = max(len(denom) for denom in standard_balances)
        print("\nWallet Balances:\n")
        print(f"{'Token':<{max_denom_length}} {'Amount':>15}")
        for denom, amount in standard_balances.items():
            print(f"{denom:<{max_denom_length}} {format_balance(amount):>15}")
        print("\n" + "=" * 40 + "\n")
    else:
        print("No balances found or an error occurred.")

def save_balances(standard_balances, file_path):
    """Save balances to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(standard_balances, file, indent=2)
        print(f"Balances saved to {file_path}")
    except Exception as e:
        print(f"Error saving balances: {e}")

def main():
    parser = argparse.ArgumentParser(description="Retrieve wallet balances.")
    parser.add_argument("--output", type=str,
                        help="File path to save balances as JSON.")

    args = parser.parse_args()

    # Hardcoded wallet address
    address = "stars1r6f5tfxdx2pw5p94f2v5n96xd4nglz5qdgl4l3"

    print(f"Fetching balances for address: {address}")
    standard_balances = get_balances(address)
    print_balances(standard_balances)

    if args.output:
        save_balances(standard_balances, args.output)

if __name__ == "__main__":
    main()
