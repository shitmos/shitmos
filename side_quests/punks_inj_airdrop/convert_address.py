# NOTE THIS DOES NOT WORK!
# IT APPEARS THAT INJECTIVE HAS A DIFFERENT WAY OF DERIVING ADDRESSES
# THE OUTPUTS ARE WRONG

import bech32

def convert_address(input_address, source_prefix, target_prefix):
    # Decode the original address
    source_hrp, data = bech32.bech32_decode(input_address)
    if source_hrp != source_prefix:
        raise ValueError("Invalid prefix for the source address")
    
    # Convert 5-bit array in Bech32 to 8-bit bytes
    decoded_bytes = bech32.convertbits(data, 5, 8, pad=False)
    if decoded_bytes is None:
        raise ValueError("Decoding failed. Check the data integrity.")

    # Re-encode these bytes to a new address with the target prefix using 5-bit encoding
    encoded_data = bech32.convertbits(decoded_bytes, 8, 5, pad=True)
    new_address = bech32.bech32_encode(target_prefix, encoded_data)
    return new_address

# Example usage:
stars1 = "stars1wtcp7m7589vdmsse30rsrlt357dwy0qygc79uf"
stars2 = "stars1c7gsk4eaelpcplg0j5urpwnzqrp6wnytematee"

new_inj1 = convert_address(stars1, "stars", "inj")
new_inj2 = convert_address(stars2, "stars", "inj")

print("New Injective Address 1:", new_inj1)
print("New Injective Address 2:", new_inj2)
