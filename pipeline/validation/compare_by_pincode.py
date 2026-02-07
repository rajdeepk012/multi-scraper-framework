
import pandas as pd
import re

def compare_addresses_by_pincode():
    """
    This script compares two Excel files of branch data based on pincode.

    The process is as follows:
    1. Load both the SFDC and the newly scraped Excel files.
    2. Define a function to extract a 6-digit pincode from an address string.
    3. Apply this function to both DataFrames to create a 'pincode' column in each.
    4. Perform an 'inner merge' on the two DataFrames. This combines them based on
       matching pincodes, creating rows for every combination of addresses that
       share a pincode.
    5. Clean up the resulting DataFrame by selecting and renaming columns for clarity.
    6. Count the number of unique pincodes that were found in both files.
    7. Save the comparison report to a new Excel file.
    """
    # --- 1. LOAD FILES ---
    try:
        sfdc_df = pd.read_excel("existing_data.xlsx")
        scraped_df = pd.read_excel("scraped_data.xlsx")
        print("Successfully loaded both Excel files.")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please make sure both Excel files are in the correct directory.")
        return

    # --- 2. EXTRACT PINCODE FUNCTION ---
    # Reasoning: A simple, reusable function to find a 6-digit pincode in a string.
    def extract_pincode(address):
        if not isinstance(address, str):
            return ''
        pincode_match = re.search(r'\b(\d{6})\b', address)
        return pincode_match.group(1) if pincode_match else ''

    # --- 3. APPLY PINCODE EXTRACTION ---
    # Reasoning: We create a dedicated 'pincode' column in both DataFrames, which makes
    # the subsequent merge operation clean and straightforward.
    sfdc_df['pincode'] = sfdc_df['Address_Line_1__c'].apply(extract_pincode)
    scraped_df['pincode'] = scraped_df['Address'].apply(extract_pincode)

    # Filter out rows where no pincode was found, as they cannot be matched.
    sfdc_df_filtered = sfdc_df[sfdc_df['pincode'] != ''].copy()
    scraped_df_filtered = scraped_df[scraped_df['pincode'] != ''].copy()

    # --- 4. MERGE DATAFRAMES ON PINCODE ---
    # Reasoning: An 'inner' merge is the most efficient way to find all records
    # that share a common value in the 'pincode' column and create the
    # side-by-side comparison.
    comparison_df = pd.merge(
        sfdc_df_filtered,
        scraped_df_filtered,
        on='pincode',
        how='inner'
    )

    # --- 5. PREPARE FINAL REPORT ---
    # Reasoning: We select only the columns the user wants to see and give them
    # clear, simple names for the final report.
    final_report_df = comparison_df[[
        'pincode',
        'Address_Line_1__c',
        'Address'
    ]].rename(columns={
        'pincode': 'Pincode',
        'Address_Line_1__c': 'SFDC_Address',
        'Address': 'Scraped_Address'
    })

    # --- 6. REPORT FINDINGS ---
    # Reasoning: The number of unique pincodes in the final report is the answer
    # to the user's question.
    matching_pincodes_count = final_report_df['Pincode'].nunique()

    print("\n--- Comparison Complete ---")
    print(f"Found {matching_pincodes_count} unique pincodes that exist in BOTH files.")
    print("---------------------------\\n")

    # --- 7. SAVE THE REPORT ---
    output_filename = 'pincode_address_comparison.xlsx'
    final_report_df.to_excel(output_filename, index=False)

    print(f"Successfully saved the comparison report to '{output_filename}'")


if __name__ == "__main__":
    compare_addresses_by_pincode()
