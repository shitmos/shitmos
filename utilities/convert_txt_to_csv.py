import csv

# Input and output file paths
input_file = "../dumb_contracts/double_dribble/sez_dribbles/conspiracy_culture/snapshots/2024-11-18/conspiracy2_2024-11-18.txt"  # Change to your text file name
output_file = "../dumb_contracts/double_dribble/sez_dribbles/conspiracy_culture/snapshots/2024-11-18/conspiracy2_2024-11-18.csv"  # Name of the CSV file to be created
delimiter = ","  # Change to your delimiter (e.g., '\t' for tab, ' ' for space)

def text_to_csv(input_file, output_file, delimiter):
    """
    Converts a text file into a CSV file.

    Args:
        input_file (str): Path to the input text file.
        output_file (str): Path to the output CSV file.
        delimiter (str): Delimiter used in the text file.
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.reader(infile, delimiter=delimiter)
            writer = csv.writer(outfile)
            
            for row in reader:
                writer.writerow(row)
        
        print(f"Conversion successful! CSV file saved as: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the conversion
text_to_csv(input_file, output_file, delimiter)
