import json
from datetime import datetime

# Get the current date in the format YYYY-MM-DD
current_date = datetime.now().strftime('%Y-%m-%d')

# Auto-generate file names based on the current date
input_file = f'snapshot_{current_date}.txt'  # Input file name (e.g., snapshot_2024-10-19.txt)
output_file = f'snapshot_{current_date}.json'  # Output file name (e.g., hamsters_snapshot_2024-10-19.json)

# Function to read wallet addresses from the input file and format them into JSON
def convert_wallets_to_json(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            wallets = [line.strip() for line in file.readlines() if line.strip()]

        if not wallets:
            print("Input file is empty or contains only whitespace.")
            return

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

    except FileNotFoundError:
        print(f"Input file {input_file} not found. Please check the file name and path.")

# Call the function to convert and save the JSON
convert_wallets_to_json(input_file, output_file)
