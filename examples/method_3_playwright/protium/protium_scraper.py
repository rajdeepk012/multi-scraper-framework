import requests
import csv
import re
import json

def main():
    url = "https://protium.co.in/visit-us/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    print(f"Fetching page: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not load the page. {e}")
        return

    # The branch data is stored in a JavaScript variable within a <script> tag.
    # This regex will find that specific script block and capture the JSON data.
    match = re.search(r'var tableData = (.*?);\n', response.text, re.S)

    if not match:
        print("Error: Could not find the branch data script block on the page. The website structure may have changed.")
        return

    # The captured data is a string that looks like JSON, but needs cleaning.
    json_string = match.group(1)
    
    try:
        # The keys in the JSON are not quoted, which is invalid. We can use a regex to add quotes.
        # This is a bit fragile but works for the current structure.
        # A more robust solution would use a library that can parse non-standard JSON if this fails.
        json_string_quoted = re.sub(r'(\s*)(\w+)(\s*): ', r'\1"\2"\3: ', json_string)
        branches_data = json.loads(json_string_quoted)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse the branch data from the script block. {e}")
        return

    # Prepare the CSV file
    csv_file = 'protium_branches.csv'
    csv_headers = ['Branch Name', 'City', 'State/UT', 'Business Hours', 'Contact Number', 'Address', 'Latitude', 'Longitude']
    
    print(f"Successfully parsed {len(branches_data)} branches. Writing to CSV...")

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        # Use '@' as the delimiter and quote all fields to handle commas in the address
        writer = csv.writer(f, delimiter='@', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(csv_headers)

        for branch in branches_data:
            # The coordinates are in the 'location' field's href attribute
            gmaps_url = branch.get('location', {}).get('href', '')
            lat, lon = "N/A", "N/A"
            coord_match = re.search(r'query=([0-9.-]+),([0-9.-]+)', gmaps_url)
            if coord_match:
                lat = coord_match.group(1)
                lon = coord_match.group(2)

            writer.writerow([
                branch.get('branch_name', 'N/A'),
                branch.get('city', 'N/A'),
                branch.get('state', 'N/A'),
                branch.get('business_hours', 'N/A'),
                branch.get('contact_number', 'N/A'),
                branch.get('address', 'N/A'),
                lat,
                lon
            ])

    print(f"\nExtraction complete. Total branches found: {len(branches_data)}. File saved as: {csv_file}")

if __name__ == "__main__":
    main()