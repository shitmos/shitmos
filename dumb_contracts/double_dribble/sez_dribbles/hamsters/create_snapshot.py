import json

# Input variables
input_file = 'snapshot_2024-09-18.txt'  # Name of the text file containing wallet addresses
output_file = 'hamsters_snapshot_2024-09-18.json'  # Name of the output JSON file

# Function to read wallet addresses from the input file and format them into JSON
def convert_wallets_to_json(input_file, output_file):
    with open(input_file, 'r') as file:
        wallets = [line.strip() for line in file.readlines()]

    # Create a list of wallet objects with token_count
    json_output = []
    token_count = 1
    for wallet in wallets:
        json_output.append({
            "owner_addr": wallet,
            "token_count": token_count,
            "is_listed": False,
        })
        token_count += 1

    # Write the JSON output to the specified file
    with open(output_file, 'w') as json_file:
        json.dump(json_output, json_file, indent=2)

    print(f"Data successfully written to {output_file}")

# Call the function to convert and save the JSON
convert_wallets_to_json(input_file, output_file)
