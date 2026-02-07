
import csv
import re
import os

# Define the input and output file paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
input_csv_path = os.path.join(script_dir, 'aavas_branches.csv')
output_csv_path = os.path.join(script_dir, 'aavas_branches_with_pincodes.csv')

# Regex to find a 6-digit number. \b ensures it matches a whole word.
pincode_regex = re.compile(r'\b(\d{6})\b')

try:
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read header and add the new 'Pincode' column
        header = next(reader)
        new_header = header + ['Pincode']
        writer.writerow(new_header)

        # Find the index of the 'Address' column
        try:
            address_index = header.index('Address')
        except ValueError:
            print("Error: 'Address' column not found in the CSV.")
            exit()

        # Process each row to find the pincode
        for row in reader:
            address = row[address_index]
            match = pincode_regex.search(address)
            
            # Extract the pincode if a match is found, otherwise leave it empty
            pincode = match.group(1) if match else ''
            
            writer.writerow(row + [pincode])

    print(f"Successfully created '{output_csv_path}' with extracted pincodes.")

except FileNotFoundError:
    print(f"Error: The file '{input_csv_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
