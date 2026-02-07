
import requests
import csv
import re

def get_cities_for_state(state):
    """Fetches the list of cities for a given state."""
    try:
        response = requests.post(
            "https://www.tvscredit.com/wp-admin/admin-ajax.php",
            data={"action": "get_state_value", "state": state}
        )
        response.raise_for_status()
        cities = re.findall(r'value="(.*?)"', response.text)
        return [city for city in cities if city]
    except requests.exceptions.RequestException as e:
        print(f"  Could not fetch cities for {state}: {e}")
        return []

def get_branches_for_city(state, city):
    """Fetches branch data for a given state and city."""
    try:
        response = requests.post(
            "https://www.tvscredit.com/wp-admin/admin-ajax.php",
            data={"action": "get_branch_locators", "state": state, "city": city}
        )
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, requests.exceptions.JSONDecodeError) as e:
        print(f"    Could not fetch branch data for {city}, {state}: {e}")
        return None

def main():
    # Hardcoded list of states from the website's HTML
    states = [
        "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Delhi", "Goa",
        "Gujarat", "Haryana", "Jharkhand", "Karnataka", "Kerala", 
        "Madhya Pradesh", "Maharashtra", "Odisha", "Pondicherry", "Punjab",
        "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh", 
        "Uttarakhand", "West Bengal"
    ]

    all_branches = []
    print("Starting TVS Credit API scraper...")

    for state in states:
        print(f"\nFetching cities for {state}...")
        cities = get_cities_for_state(state)
        if not cities:
            print(f"  No cities found for {state}.")
            continue
        
        print(f"  Found {len(cities)} cities.")

        for city in cities:
            print(f"  - Fetching branches for {city}, {state}")
            branch_data = get_branches_for_city(state, city)

            if branch_data and 'markers' in branch_data:
                for i, address_html in enumerate(branch_data.get('address', [])):
                    marker = branch_data['markers'][i]
                    # Use regex for more robust parsing
                    address_match = re.search(r"<p><i class='fas fa-map-marker-alt'></i>(.*?)</p>", address_html)
                    address = address_match.group(1).strip() if address_match else "N/A"

                    url_match = re.search(r"href='(.*?)'", address_html)
                    google_maps_url = url_match.group(1) if url_match else "N/A"

                    all_branches.append({
                        "State": state,
                        "City": city,
                        "Address": address,
                        "Latitude": marker.get('lat'),
                        "Longitude": marker.get('lng'),
                        "Google_Maps_URL": google_maps_url
                    })

    # Save to CSV
    csv_file = 'tvs_credit_branches.csv'
    csv_headers = ["State", "City", "Address", "Latitude", "Longitude", "Google_Maps_URL"]
    print(f"\nWriting {len(all_branches)} branches to {csv_file}...")
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers, delimiter='@')
        writer.writeheader()
        writer.writerows(all_branches)
    print("Scraping complete.")

if __name__ == "__main__":
    main()
