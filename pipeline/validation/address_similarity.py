
import pandas as pd
from thefuzz import fuzz

def calculate_similarity_score():
    """
    This script reads the pincode comparison report and calculates a similarity
    score for the addresses in each row.

    The process is as follows:
    1. Load the 'pincode_address_comparison.xlsx' file.
    2. Use the 'fuzz.token_sort_ratio' method from the 'thefuzz' library.
       This method is ideal for addresses because it ignores word order and is
       resilient to minor typos or differences.
    3. Apply this function to the 'SFDC_Address' and 'Scraped_Address' columns.
    4. Create a new column, 'Similarity_Score', with the resulting score (0-100).
    5. Save the new DataFrame, with the score, to a new Excel file.
    """
    input_filename = "pincode_address_comparison.xlsx"

    # --- 1. LOAD FILE ---
    try:
        df = pd.read_excel(input_filename)
        print(f"Successfully loaded '{input_filename}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found. Please run the previous step first.")
        return

    # --- 2. DEFINE SIMILARITY CALCULATION ---
    # Reasoning: We define a small wrapper function to handle potential non-string
    # data and to clearly name the method we are using (Token Sort Ratio).
    def get_token_sort_ratio(addr1, addr2):
        # Ensure both inputs are strings before comparing
        if not isinstance(addr1, str) or not isinstance(addr2, str):
            return 0
        return fuzz.token_sort_ratio(addr1, addr2)

    # --- 3. APPLY THE FUNCTION ---
    # Reasoning: We use the .apply() method with a lambda function to efficiently
    # run our calculation across every row in the DataFrame.
    print("Calculating similarity scores for each address pair...")
    df['Similarity_Score'] = df.apply(
        lambda row: get_token_sort_ratio(row['SFDC_Address'], row['Scraped_Address']),
        axis=1
    )

    # --- 4. SAVE THE FINAL REPORT ---
    output_filename = "pincode_comparison_with_scores.xlsx"
    df.to_excel(output_filename, index=False)

    print(f"\nSuccessfully calculated scores and saved the report to '{output_filename}'.")
    print("You can now open this file and sort by 'Similarity_Score' to see the best and worst matches.")

if __name__ == "__main__":
    calculate_similarity_score()
