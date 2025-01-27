import csv
import os

def process_csv_files(input_files, output_file):
    combined_list = []

    # Process each CSV file
    for file in input_files:
        try:
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row:  # Ensure the row is not empty
                        combined_list.append(row[0])  # Keep only the first field
        except Exception as e:
            print(f"Error processing {file}: {e}")

    # Write the combined list to the output .txt file
    try:
        with open(output_file, 'w') as txtfile:
            for item in combined_list:
                txtfile.write(f"{item}\n")
        print(f"Combined list written to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

# Example usage
if __name__ == "__main__":
    # List of input CSV files
    input_files = ["tier3_1.csv", "tier3_2.csv", "tier3_3.csv", "tier3_4.csv", "tier3_5.csv", "tier3_6.csv"]  # Replace with your file paths

    # Output .txt file
    output_file = "tier3.txt"

    process_csv_files(input_files, output_file)
