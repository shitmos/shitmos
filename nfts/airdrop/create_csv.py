import csv

def main():
    input_file = 'wallets_top_150.txt'
    output_file = 'wallets_with_amount.csv'

    with open(input_file, 'r') as file:
        addresses = file.readlines()
    
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['address', 'amount'])
        # Write each address with the amount 1
        for address in addresses:
            address = address.strip()  # Clean the address
            if address:  # Only proceed if the address is not empty
                writer.writerow([address, 1])

    print(f"CSV file created successfully: {output_file}")

if __name__ == '__main__':
    main()
