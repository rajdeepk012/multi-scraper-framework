import csv
import requests
import re

def get_final_url_and_coords(short_url):
    """Follows a short URL, gets the final redirected URL, and parses coordinates from it."""
    try:
        # Use a common browser user-agent
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        response = requests.get(short_url, headers=headers, timeout=15, allow_redirects=True)
        final_url = response.url
        
        # New regex to find coordinates in the final URL, e.g., /@-12.345,67.890,
        match = re.search(r'/@(-?[0-9\.]+),(-?[0-9\.]+),', final_url)
        
        if match:
            lat = match.group(1)
            lon = match.group(2)
            return final_url, lat, lon
        else:
            return final_url, "N/A", "N/A"
            
    except requests.exceptions.RequestException as e:
        print(f"  - Could not process URL {short_url}: {e}")
        return short_url, "N/A", "N/A"

def main():
    input_csv = 'protium_branches.csv'
    output_csv = 'protium_branches_with_coords.csv'

    print(f"Reading from {input_csv}...")
    
    try:
        with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
             open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.reader(infile, delimiter='@')
            writer = csv.writer(outfile, delimiter='@', quotechar='"', quoting=csv.QUOTE_ALL)
            
            headers = next(reader) # Read the header row
            writer.writerow(headers) # Write headers to the new file
            
            print("Processing branches...")
            processed_count = 0
            for row in reader:
                # The Location URL is the last column
                location_url_index = len(headers) - 1
                short_url = row[location_url_index]
                
                final_url, lat, lon = get_final_url_and_coords(short_url)
                
                # Update the row with the new data
                row[location_url_index] = final_url
                row[location_url_index - 2] = lat # Update Latitude
                row[location_url_index - 1] = lon # Update Longitude
                
                writer.writerow(row)
                processed_count += 1
                if processed_count % 10 == 0:
                    print(f"  ...processed {processed_count} branches.")

            print(f"\nProcessing complete. Corrected data saved to {output_csv}")

    except FileNotFoundError:
        print(f"Error: The input file '{input_csv}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
