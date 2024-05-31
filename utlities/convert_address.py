import bech32

def convert_address(stargaze_address, target_prefix="osmo"):
    """
    Convert a Stargaze address to an Osmosis address.
    """
    hrp, data = bech32.bech32_decode(stargaze_address)
    if data is None:
        raise ValueError("Invalid Stargaze address.")
    osmosis_address = bech32.bech32_encode(target_prefix, data)
    return osmosis_address

def main():
    stargaze_address = input("Please enter the Stargaze address to convert: ")
    try:
        osmosis_address = convert_address(stargaze_address)
        print(f"Osmosis Address: {osmosis_address}")
    except ValueError as e:
        print(str(e))

if __name__ == "__main__":
    main()
