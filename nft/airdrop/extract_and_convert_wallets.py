from bech32 import bech32_decode, bech32_encode, convertbits

# Define input and output file names
input_file = 'smart_stake_top_150.txt'
output_file = 'wallets_top_150.txt'

def convert_osmo_to_stars(osmo_address):
    # Decode the osmo address
    hrp, data = bech32_decode(osmo_address)
    if data is None or hrp != 'osmo':
        raise ValueError("Invalid Osmosis address")
    
    # Convert the data from 5-bit to 8-bit, and then back to 5-bit
    data_converted = convertbits(data, 5, 8, pad=True)
    if data_converted is None:
        raise ValueError("Failed to convert data bits")
    data_reconverted = convertbits(data_converted, 8, 5, pad=True)
    if data_reconverted is None:
        raise ValueError("Failed to reconvert data bits")
    
    # Re-encode with the 'stars' prefix
    stars_address = bech32_encode('stars', data_reconverted)
    return stars_address

# Function to extract osmosis wallets and convert them to stargaze wallets
def extract_and_convert_wallets(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    stargaze_wallets = []
    for line in lines:
        parts = line.split()
        for part in parts:
            if part.startswith('osmo'):
                try:
                    stargaze_wallet = convert_osmo_to_stars(part)
                    stargaze_wallets.append(stargaze_wallet)
                except ValueError as e:
                    print(f"Skipping invalid address {part}: {e}")
                break  # Stop after finding the osmo wallet in the line

    with open(output_file, 'w') as outfile:
        for wallet in stargaze_wallets:
            outfile.write(wallet + '\n')

# Call the function to process the file
extract_and_convert_wallets(input_file, output_file)

print(f"Stargaze wallets have been extracted and written to {output_file}")
