#!/usr/bin/env python3
# convert_addresses.py
# Usage: python3 convert_addresses.py input.txt output_osmo.txt
# Requires: pip install bech32

import sys
from bech32 import bech32_decode, bech32_encode, convertbits

def convert_prefix(addr, new_hrp):
    hrp, data = bech32_decode(addr)
    if hrp is None or data is None:
        raise ValueError(f"invalid bech32 address: {addr}")
    # convert from 5-bit groups -> bytes (8-bit)
    decoded = convertbits(data, 5, 8, False)
    if decoded is None:
        raise ValueError("convertbits decode failed")
    # convert back to 5-bit groups for new prefix
    new_data = convertbits(decoded, 8, 5, True)
    if new_data is None:
        raise ValueError("convertbits encode failed")
    return bech32_encode(new_hrp, new_data)

def main():
    if len(sys.argv) < 3:
        print("Usage: convert_addresses.py input.txt output_osmo.txt")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2]
    with open(inp, "r") as f:
        lines = [l.strip() for l in f if l.strip()]
    converted = []
    for a in lines:
        try:
            c = convert_prefix(a, "osmo")  # osmosis account prefix
            converted.append(c)
        except Exception as e:
            print(f"ERROR converting {a}: {e}")
    with open(out, "w") as f:
        f.write("\n".join(converted))
    print(f"Wrote {len(converted)} addresses to {out}")

if __name__ == "__main__":
    main()
