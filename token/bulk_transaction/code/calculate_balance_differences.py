import json
import sys

def load_balances(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_differences(initial_balances, final_balances):
    differences = {}
    for denom, initial_amount in initial_balances.items():
        final_amount = final_balances.get(denom, 0)
        differences[denom] = final_amount - initial_amount
    return differences

def print_differences(differences):
    print("Balance differences:")
    for denom, difference in differences.items():
        print(f"{denom}: {difference}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python calculate_balance_differences.py <initial_balances.json> <final_balances.json>")
        sys.exit(1)

    initial_balances_path = sys.argv[1]
    final_balances_path = sys.argv[2]

    initial_balances = load_balances(initial_balances_path)
    final_balances = load_balances(final_balances_path)

    differences = calculate_differences(initial_balances, final_balances)
    print_differences(differences)
