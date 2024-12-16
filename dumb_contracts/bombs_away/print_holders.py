import os
import json
import csv
import matplotlib.pyplot as plt
import numpy as np

# Configuration
TOKEN_DENOM = "factory/osmo1n6asrjy9754q8y9jsxqf557zmsv3s3xa5m9eg5/uspice"  # Denom for the token
DECIMALS = 6  # Number of decimals for the token
EXPECTED_CIRCULATION = 10_000_000.0  # Replace with the expected total token supply

# Paths
OUTPUT_JSON = "output.json"
OUTPUT_CSV = "holders.csv"

# Run the osmosisd command
OSMOSISD_COMMAND = (
    f"osmosisd q bank denom-owners {TOKEN_DENOM} "
    "--node https://rpc.osmosis.zone --page-limit 2000 -o json > output.json 2>&1"
)
print("Running osmosisd command...")
os.system(OSMOSISD_COMMAND)
print("Command executed.")

# Load JSON
try:
    with open(OUTPUT_JSON, "r") as file:
        data = json.load(file)
    print("JSON loaded successfully.")
except Exception as e:
    print(f"Failed to load JSON: {e}")
    exit(1)

# Extract holders
holders = data.get("denom_owners", [])
if not holders:
    print("No holders found in the JSON.")
    exit(1)

# Parse data into CSV
parsed_data = []
total_balance = 0  # To calculate the total amount held by all addresses
try:
    for h in holders:
        address = h["address"]
        balance = int(h["balance"]["amount"]) / (10 ** DECIMALS)  # Adjust for decimals
        formatted_balance = f"{balance:.{DECIMALS}f}"  # Ensure consistent decimal formatting
        parsed_data.append({"address": address, "balance": float(formatted_balance)})
        total_balance += balance
    with open(OUTPUT_CSV, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["address", "balance"])
        writer.writeheader()
        writer.writerows(parsed_data)
    print(f"CSV saved as {OUTPUT_CSV}")
except Exception as e:
    print(f"Error while parsing data: {e}")
    exit(1)

# Compare total balance with expected circulation
print("\nTotal Balance Held:")
print(f"{total_balance:.6f} (Expected: {EXPECTED_CIRCULATION:.6f})")
if abs(total_balance - EXPECTED_CIRCULATION) < 1e-6:
    print("Total balance matches the expected circulation.")
else:
    print("Warning: Total balance does NOT match the expected circulation!")

# Print Basic Token Distribution
bins = {
    "Less than 1": 0,
    "1-10": 0,
    "11-100": 0,
    "101-1000": 0,
    "1001-10000": 0,
    "10001-100000": 0,
    "100001-1000000": 0,
    "1000001+": 0,
}
try:
    for holder in parsed_data:
        balance = holder["balance"]
        if balance < 1:
            bins["Less than 1"] += 1
        elif 1 <= balance <= 10:
            bins["1-10"] += 1
        elif 11 <= balance <= 100:
            bins["11-100"] += 1
        elif 101 <= balance <= 1000:
            bins["101-1000"] += 1
        elif 1001 <= balance <= 10000:
            bins["1001-10000"] += 1
        elif 10001 <= balance <= 100000:
            bins["10001-100000"] += 1
        elif 100001 <= balance <= 1000000:
            bins["100001-1000000"] += 1
        else:
            bins["1000001+"] += 1

    # Print summary statistics
    print("\nSummary Statistics:")
    for bin_range, count in bins.items():
        print(f"{bin_range}: {count} holders")
    print(f"Total Holders: {len(parsed_data)}")
except Exception as e:
    print(f"Error during bin categorization: {e}")
    exit(1)

# Print Top 10 Holders
try:
    # Sort by balance
    sorted_holders = sorted(parsed_data, key=lambda x: x["balance"], reverse=True)
    top_10_holders = sorted_holders[:10]
    top_10_total = sum([holder["balance"] for holder in top_10_holders])
    top_10_percentage = (top_10_total / total_balance) * 100

    print("\nTop 10 Holders:")
    for i, holder in enumerate(top_10_holders, start=1):
        print(f"{i}. {holder['address']}: {holder['balance']:.{DECIMALS}f}")
    print(f"Top 10 Holders Total: {top_10_total:.{DECIMALS}f} ({top_10_percentage:.2f}% of total supply)")
except Exception as e:
    print(f"Error while calculating top 10 holders: {e}")
    exit(1)

# Generate Bar Graph with Cumulative Overlay
try:
    # Sort balances (descending order)
    balances = sorted([float(h["balance"]) for h in parsed_data], reverse=True)
    cumulative_balances = np.cumsum(balances) / total_balance * 100  # Cumulative percentage

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Bar graph for individual balances
    ax1.bar(range(len(balances)), balances, color="blue", alpha=0.6, label="Tokens Held")
    ax1.set_xlabel("Wallets (sorted by balance)", fontsize=12)
    ax1.set_ylabel("Tokens Held", color="blue", fontsize=12)
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.set_yscale("log")  # Log scale for better visualization of small balances

    # Line graph for cumulative percentage
    ax2 = ax1.twinx()
    ax2.plot(range(len(cumulative_balances)), cumulative_balances, color="red", linestyle="-", linewidth=2, label="Cumulative %")
    ax2.set_ylabel("Cumulative Percentage (%)", color="red", fontsize=12)
    ax2.tick_params(axis="y", labelcolor="red")
    ax2.set_ylim(0, 100)  # Percentage scale

    # Title and legends
    fig.suptitle("Token Distribution: Balances and Cumulative Percentage", fontsize=14)
    fig.tight_layout()
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Save and show the plot
    plt.savefig("distribution_with_cumulative.png")
    print("Combined graph saved as 'distribution_with_cumulative.png'.")
    plt.show()
except Exception as e:
    print(f"Error during plotting: {e}")
    exit(1)
