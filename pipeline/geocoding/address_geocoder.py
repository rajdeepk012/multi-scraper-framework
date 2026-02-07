
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GOOGLE_GEOCODE_API_KEY")
if not API_KEY:
    raise ValueError("Google Geocoding API key not found in .env file. Please add GOOGLE_GEOCODE_API_KEY.")

INPUT_FILE = '../samples/sample_input.csv'
OUTPUT_FILE = '../samples/sample_geocoded.csv'
ADDRESS_COLUMN = 'Address'
MAX_ROWS = None  # Set to None to process all rows

def geocode_address(address):
    """
    Geocodes a single address using the Google Geocoding API.
    """
    if not address or not isinstance(address, str) or address.strip() == '':
        return {
            'api_formatted_address': None,
            'api_pincode': None,
            'api_city': None,
            'api_state': None,
            'api_lat': None,
            'api_lng': None
        }

    geo_data = {
        'api_formatted_address': None,
        'api_pincode': None,
        'api_city': None,
        'api_state': None,
        'api_lat': None,
        'api_lng': None
    }

    params = {
        'address': address,
        'key': API_KEY
    }
    try:
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        results = response.json().get('results', [])

        if not results:
            return geo_data

        # Best result is usually the first one
        top_result = results[0]
        address_components = top_result.get('address_components', [])
        geo_data['api_formatted_address'] = top_result.get('formatted_address')

        # Extract location
        location = top_result.get('geometry', {}).get('location', {})
        geo_data['api_lat'] = location.get('lat')
        geo_data['api_lng'] = location.get('lng')

        # Extract address components
        for component in address_components:
            types = component.get('types', [])
            if 'postal_code' in types:
                geo_data['api_pincode'] = component.get('long_name')
            if 'locality' in types:
                geo_data['api_city'] = component.get('long_name')
            if 'administrative_area_level_1' in types:
                geo_data['api_state'] = component.get('long_name')
        
        return geo_data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during API request: {e}")
        return geo_data
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return geo_data

def main():
    print(f"Reading data from {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: The file {INPUT_FILE} was not found.")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    if MAX_ROWS:
        df = df.head(MAX_ROWS)
        print(f"Debug run: limiting processing to the first {len(df)} rows.")

    print("Geocoding addresses using Google API...")
    api_results = []
    total_rows = len(df)
    for index, row in df.iterrows():
        print(f"Processing row {index + 1}/{total_rows}...")
        address_to_geocode = row[ADDRESS_COLUMN]
        geo_data = geocode_address(address_to_geocode)
        api_results.append(geo_data)
        # Rate limiting to stay within typical free tier usage limits
        time.sleep(0.05)

    # Convert list of dicts to DataFrame
    api_df = pd.DataFrame(api_results)

    # Combine the new API data with the original DataFrame
    df_final = pd.concat([df, api_df], axis=1)

    print(f"Saving enriched data to {OUTPUT_FILE}...")
    try:
        df_final.to_csv(OUTPUT_FILE, index=False)
        print(f"Processing complete. The file has been updated successfully and saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == "__main__":
    main()
