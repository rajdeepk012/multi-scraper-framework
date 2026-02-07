
import requests
import csv
import json

def extract_aavas_data():
    states = [
        "CHHATTISGARH", "DELHI", "GUJARAT", "HARYANA", "HIMACHAL%20PRADESH",
        "KARNATAKA", "MADHYA%20PRADESH", "MAHARASHTRA", "ODISHA", "PUNJAB",
        "RAJASTHAN", "TAMIL%20NADU", "UTTAR%20PRADESH", "UTTARAKHAND"
    ]

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # NOTE: Obtain fresh PHPSESSID and csrfToken by visiting https://www.aavas.in/branch-locator
        'Cookie': 'PHPSESSID=YOUR_SESSION_ID; csrfToken=YOUR_CSRF_TOKEN'
    }

    all_branches_data = []

    for state in states:
        print(f"Fetching branches for {state.replace('%20', ' ')}...")
        try:
            state_url = f"https://www.aavas.in/ajax-branch-by-state?id={state}"
            response = requests.get(state_url, headers=headers)
            response.raise_for_status()
            branches_in_state = response.json()

            for branch_summary in branches_in_state:
                branch_id = branch_summary.get('id')
                if not branch_id:
                    continue

                branch_url = f"https://www.aavas.in/branch-pin-code?id={branch_id}&type=state"
                branch_response = requests.get(branch_url, headers=headers)
                branch_response.raise_for_status()
                branch_details_list = branch_response.json()

                if branch_details_list:
                    branch_details = branch_details_list[0]
                    all_branches_data.append([
                        branch_details.get('state_name', 'NA'),
                        branch_details.get('branch_city', 'NA'),
                        branch_details.get('branch_name', 'NA'),
                        branch_details.get('branch_address', 'NA'),
                        branch_details.get('latitude', 'NA'),
                        branch_details.get('longitude', 'NA')
                    ])
        except requests.exceptions.RequestException as e:
            print(f"Could not fetch data for state {state}: {e}")
        except json.JSONDecodeError as e:
            print(f"Could not parse JSON for state {state}: {e}")

    # Write to CSV
    with open('aavas_branches.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['State', 'City', 'Branch', 'Address', 'Latitude', 'Longitude'])
        writer.writerows(all_branches_data)
    
    print(f"\nSuccessfully extracted {len(all_branches_data)} branches to aavas_branches.csv")

if __name__ == '__main__':
    extract_aavas_data()
