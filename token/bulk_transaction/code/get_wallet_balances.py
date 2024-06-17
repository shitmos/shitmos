import argparse
import json
import subprocess
import config

def convert_micro_to_unit(micro_amount):
    return micro_amount / config.CONVERSION_RATE

def format_balance(amount):
    return f"{amount:,.2f}"

def get_balances(wallet_name, keyring_backend):
    try:
        address = subprocess.check_output(
            ["osmosisd", "keys", "show", wallet_name, "-a", "--keyring-backend", keyring_backend]
        ).decode("utf-8").strip()

        balances_raw = subprocess.check_output(
            ["osmosisd", "query", "bank", "balances", address, "-o", "json"]
        ).decode("utf-8")

        balances_json = json.loads(balances_raw)
        balances = balances_json.get("balances", [])

        standard_balances = {}
        for balance in balances:
            denom = balance.get("denom")
            amount_micro = int(balance.get("amount"))
            amount_standard = convert_micro_to_unit(amount_micro)
            common_name = config.TOKEN_NAME_MAPPING.get(denom, denom)
            standard_balances[common_name] = amount_standard

        return standard_balances
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return {}

def print_balances(standard_balances):
    if standard_balances:
        # Calculate USD values and sort by USD amount
        usd_balances = {
            denom: amount * config.EXCHANGE_RATES.get(denom, config.DEFAULT_EXCHANGE_RATE)
            for denom, amount in standard_balances.items()
        }
        sorted_balances = sorted(standard_balances.items(), key=lambda x: usd_balances[x[0]], reverse=True)

        # Calculate total USD balance
        total_usd_balance = sum(usd_balances.values())

        # Print top emoji row
        print("\n💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩\n")

        # Print indented header
        print(" Shitmos Economic Zone wallet balances:\n")

        # Determine the longest token name for formatting
        max_denom_length = max(len(denom) for denom in standard_balances)

        # Print balances in standard units
        for denom, amount in sorted_balances:
            formatted_amount = format_balance(amount)
            print(f" {denom:<{max_denom_length}} : {formatted_amount:>15} {denom}")

        print("\n Balances in USD:\n")

        # Print balances in USD
        for denom, amount in sorted_balances:
            usd_amount = usd_balances[denom]
            formatted_usd_amount = format_balance(usd_amount)
            print(f" {denom:<{max_denom_length}} : {'$':>2}{formatted_usd_amount:>15} USD")

        # Print underline, total, and double underline
        print(" " + "-" * (max_denom_length + 22))
        print(f" {'TOTAL':<{max_denom_length}} : {'$':>2}{format_balance(total_usd_balance):>15} USD")
        print(" " + "=" * (max_denom_length + 22))

        # Print closing blank row and bottom emoji row
        print("\n💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩\n")
    else:
        print("No balances found or an error occurred.")

def save_balances(standard_balances, file_path):
    with open(file_path, 'w') as file:
        json.dump(standard_balances, file, indent=2)

def main():
    # Default values
    default_wallet_name = "shitmos_nft"
    default_keyring_backend = "file"

    parser = argparse.ArgumentParser(description="Get wallet balances.")
    parser.add_argument("wallet_name", nargs='?', default=default_wallet_name, type=str, help="The name of the wallet.")
    parser.add_argument("--keyring-backend", type=str, default=default_keyring_backend, help="The keyring backend to use (default: file).")
    parser.add_argument("--output", type=str, help="The file path to save balances as JSON.")

    args = parser.parse_args()

    standard_balances = get_balances(args.wallet_name, args.keyring_backend)
    print_balances(standard_balances)
    
    if args.output:
        save_balances(standard_balances, args.output)

if __name__ == "__main__":
    main()
