import sys
from bech32 import bech32_decode, bech32_encode, convertbits

def convert_address(address):
    hrp, data = bech32_decode(address)
    if hrp is None or data is None:
        raise ValueError("Invalid Bech32 address")

    # Convert 5-bit data back to 8-bit data
    decoded_data = convertbits(data, 5, 8, False)
    if decoded_data is None:
        raise ValueError("Error in data conversion")

    # Encode the data to the new Bech32 format with 'osmo' prefix
    new_address = bech32_encode('osmo', convertbits(decoded_data, 8, 5, True))
    if new_address is None:
        raise ValueError("Error in address encoding")

    return new_address

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_address.py <stars_address>")
        sys.exit(1)

    stars_address = sys.argv[1]
    try:
        osmo_address = convert_address(stars_address)
        print(f"Converted address: {osmo_address}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
