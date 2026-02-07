
import pandas as pd
import re
import numpy as np

def find_duplicates():
    """
    This script finds and removes duplicate branch records by comparing a file of newly
    scraped branches against an existing Salesforce (SFDC) data file.

    The process is as follows:
    1. Load both the SFDC and the newly scraped Excel files into pandas DataFrames.
    2. Define a normalization function that cleans up address strings and extracts the pincode.
       - It converts text to lowercase.
       - It removes punctuation and extra whitespace.
       - It uses a regular expression to find a 6-digit pincode.
    3. Apply this function to both DataFrames to create standardized columns for comparison.
    4. Create a unique 'match_key' in each DataFrame by combining the normalized address and pincode.
    5. Compare the keys from the new data with the keys from the SFDC data to find duplicates.
    6. Print a summary: total new records, number of duplicates found, and number of unique records.
    7. Save the unique, non-duplicate records to a new Excel file.
    """
    # --- 1. LOAD FILES ---
    # Reasoning: We need to load the data from the Excel files into memory to work with it.
    # pandas DataFrames are the standard tool for this in Python.
    try:
        sfdc_df = pd.read_excel("existing_data.xlsx")
        scraped_df = pd.read_excel("scraped_data.xlsx")
        print("Successfully loaded both Excel files.")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please make sure both Excel files are in the correct directory.")
        return

    # --- 2. NORMALIZE DATA FUNCTION ---
    # Reasoning: Address data is often inconsistent. A normalization function ensures we compare
    # apples to apples by cleaning the text and extracting the most reliable part (the pincode).
    def normalize_and_extract_pincode(address):
        # Handle cases where the address might be missing (not a string)
        if not isinstance(address, str):
            return '', '' # Return empty strings for non-string inputs

        # Convert to lowercase and remove leading/trailing whitespace
        clean_address = address.lower().strip()

        # Extract 6-digit pincode using regular expressions
        # \b ensures we match a whole word (boundary), so we don't match 6 digits inside a longer number.
        pincode_match = re.search(r'\b(\d{6})\b', clean_address)
        pincode = pincode_match.group(1) if pincode_match else ''

        # Remove all non-alphanumeric characters (except spaces) to make matching more flexible
        # For example, "123, main st." becomes "123 main st"
        clean_address = re.sub(r'[^a-z0-9\s]', '', clean_address)
        # Replace multiple spaces with a single space
        clean_address = re.sub(r'\s+', ' ', clean_address).strip()

        return clean_address, pincode

    # --- 3. APPLY NORMALIZATION ---
    # Reasoning: We apply the cleaning function to the relevant address columns in both DataFrames
    # to prepare them for comparison.

    # For SFDC data, the column is 'Address_Line_1__c'
    sfdc_df[['clean_address', 'pincode']] = sfdc_df['Address_Line_1__c'].apply(
        lambda x: pd.Series(normalize_and_extract_pincode(x))
    )

    # For the scraped data, the column is 'Address'
    scraped_df[['clean_address', 'pincode']] = scraped_df['Address'].apply(
        lambda x: pd.Series(normalize_and_extract_pincode(x))
    )

    # --- 4. CREATE MATCH KEY ---
    # Reasoning: A combined key of address + pincode is much more likely to be unique and
    # reliable for matching than either part alone.
    sfdc_df['match_key'] = sfdc_df['clean_address'] + '_' + sfdc_df['pincode']
    scraped_df['match_key'] = scraped_df['clean_address'] + '_' + scraped_df['pincode']

    # Create a set of SFDC keys for efficient lookup.
    # Reasoning: Checking for an item in a set is much faster (O(1) average time complexity)
    # than checking in a list or DataFrame column (O(n)).
    sfdc_keys = set(sfdc_df['match_key'])

    # --- 5. IDENTIFY DUPLICATES ---
    # Reasoning: The `isin()` method checks each 'match_key' from the scraped data to see if it
    # exists in the set of SFDC keys. It returns a boolean Series (True for duplicates, False for unique).
    scraped_df['is_duplicate'] = scraped_df['match_key'].isin(sfdc_keys)

    # --- 6. REPORT FINDINGS ---
    total_scraped = len(scraped_df)
    duplicates_found = scraped_df['is_duplicate'].sum()
    unique_records = total_scraped - duplicates_found

    print("\n--- Analysis Complete ---")
    print(f"Total records in newly scraped file: {total_scraped}")
    print(f"Number of duplicate records found in SFDC data: {duplicates_found}")
    print(f"Number of new, unique records to be added: {unique_records}")
    print("-------------------------\n")

    # --- 7. SAVE UNIQUE RECORDS ---
    # Reasoning: We save only the non-duplicate records to a new file, providing a clean
    # dataset for the user and preserving the original files.
    unique_df = scraped_df[scraped_df['is_duplicate'] == False].copy()

    # Remove the temporary helper columns before saving
    unique_df.drop(columns=['clean_address', 'pincode', 'match_key', 'is_duplicate'], inplace=True)

    output_filename = 'unique_branches_to_add.xlsx'
    unique_df.to_excel(output_filename, index=False)

    print(f"Successfully saved {unique_records} unique records to '{output_filename}'")


if __name__ == "__main__":
    # This allows the script to be run directly from the command line.
    find_duplicates()
