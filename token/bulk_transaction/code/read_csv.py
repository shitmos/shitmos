import pandas as pd

# Path to the snapshot CSV file
file_path = '../data/snapshots/snapshot_2024-06-09.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Display the first few rows of the DataFrame
print(df.head())
