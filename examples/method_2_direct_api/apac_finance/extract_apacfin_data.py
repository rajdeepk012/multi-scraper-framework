
import requests
import csv
import json
import re

def get_branch_details(branch_id):
    url = f"https://apacfin.com/findPincode?id={branch_id}"
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for branch ID {branch_id}: {e}")
        return None

def get_branches_for_state(state_id):
    url = f"https://apacfin.com/findBranch?id={state_id}"
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching branches for state ID {state_id}: {e}")
        return []

def main():
    states = {
        "1": "Maharashtra",
        "3": "Karnataka",
        "5": "Andhra Pradesh"
    }

    with open('apacfin_branches.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['State', 'City/Branch', 'Address', 'Embedded Map Link'])

        for state_id, state_name in states.items():
            print(f"Fetching branches for {state_name}...")
            branches = get_branches_for_state(state_id)

            for branch in branches:
                branch_id = branch.get('id')
                branch_name = branch.get('branch')
                
                if not branch_id:
                    continue

                details = get_branch_details(branch_id)
                if details:
                    address = details.get('branch_address', 'NA')
                    map_link_html = details.get('embedded', 'NA')
                    
                    # Extract the src URL from the iframe
                    src_link = 'NA'
                    if map_link_html and 'src=' in map_link_html:
                        match = re.search(r'src="(.*?)"', map_link_html)
                        if match:
                            src_link = match.group(1)

                    writer.writerow([state_name, branch_name, address, src_link])
    
    print("Successfully extracted all branch data to apacfin_branches.csv")

if __name__ == '__main__':
    main()
