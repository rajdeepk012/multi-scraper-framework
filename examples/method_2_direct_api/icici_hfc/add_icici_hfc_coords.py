import requests
import csv
import os
from dotenv import load_dotenv

def add_coordinates_to_icici_hfc_data():
    """Adds latitude and longitude to the ICICI HFC branches CSV using Google Geocoding API."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_GEOCODE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_GEOCODE_API_KEY not found in .env file.")
        return

    input_filename = "icici_hfc_branches.csv"
    output_filename = "icici_hfc_branches_with_coords.csv"
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile, delimiter='@')
            header = next(reader) # Skip header
            data = list(reader)
    except FileNotFoundError:
        print(f"Error: {input_filename} not found.")
        return

    updated_data = []
    updated_header = header + ["Latitude", "Longitude"]

    for row in data:
        address = row[2] # Address is in the 3rd column
        print(f"Geocoding address: {address}")

        params = {
            "address": address,
            "key": api_key
        }

        try:
            response = requests.get(base_url, params=params, timeout=15)
            response.raise_for_status()
            geocode_result = response.json()

            if geocode_result['status'] == 'OK':
                location = geocode_result['results'][0]['geometry']['location']
                lat = location['lat']
                lng = location['lng']
                row.extend([lat, lng])
            else:
                print(f"Could not geocode address: {address}. Status: {geocode_result['status']}")
                row.extend(['NA', 'NA'])
        except requests.exceptions.RequestException as e:
            print(f"Error during geocoding request for {address}: {e}")
            row.extend(['NA', 'NA'])
        except (KeyError, IndexError) as e:
            print(f"Error parsing geocode response for {address}: {e}")
            row.extend(['NA', 'NA'])
        
        updated_data.append(row)

    # Save the updated data
    with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter='@')
        writer.writerow(updated_header)
        writer.writerows(updated_data)
    print(f"Data with coordinates saved to {output_filename}")

if __name__ == "__main__":
    add_coordinates_to_icici_hfc_data()
