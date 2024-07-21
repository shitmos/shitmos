import bech32

def convert_address(address, target_prefix):
    """
    Convert a Bech32 address to another Bech32 address with a different prefix.
    """
    hrp, data = bech32.bech32_decode(address)
    if data is None:
        raise ValueError(f"Invalid address for {hrp}.")
    new_address = bech32.bech32_encode(target_prefix, data)
    return new_address

def main():
    direction = input("Enter conversion direction (1 for Stargaze to Osmosis, 2 for Osmosis to Stargaze): ")
    if direction == '1':
        stargaze_address = input("Please enter the Stargaze address to convert: ")
        try:
            osmosis_address = convert_address(stargaze_address, "osmo")
            print(f"Osmosis Address: {osmosis_address}")
        except ValueError as e:
            print(str(e))
    elif direction == '2':
        osmosis_address = input("Please enter the Osmosis address to convert: ")
        try:
            stargaze_address = convert_address(osmosis_address, "stars")
            print(f"Stargaze Address: {stargaze_address}")
        except ValueError as e:
            print(str(e))
    else:
        print("Invalid direction. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
