import pandas as pd

# Load the addresses from the CSV file
addresses_file = 'clout_addresses.csv'

try:
    df = pd.read_csv(addresses_file)

    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("The addresses file is empty.")

    # Ensure there is an 'address' column
    if 'address' not in df.columns:
        raise ValueError("The CSV file must contain an 'address' column.")

    # Convert the first character of each address to lowercase
    df['address'] = df['address'].apply(lambda x: x[0].lower() + x[1:] if pd.notnull(x) else x)

    # Save the modified addresses back to the CSV file
    df.to_csv(addresses_file, index=False)

    print("All addresses have been updated to start with a lowercase character.")
except FileNotFoundError:
    print(f"Error: The file '{addresses_file}' does not exist.")
except pd.errors.EmptyDataError:
    print(f"Error: The file '{addresses_file}' is empty or improperly formatted.")
except ValueError as ve:
    print(f"Error: {ve}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
