import csv
import json
import re

def extract_shubham_data(html_file, csv_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Aggressive regex to capture the content within the script tag
    match = re.search(r'<script>\s*self\.__next_f\.push\(\[1, "b:(.*?)"\]\).*?<\/script>', html_content, re.DOTALL)
    if not match:
        print("Could not find the data variable in the HTML file.")
        return

    # The captured group contains the JSON-like data, but it's escaped.
    # We need to unescape it before parsing.
    json_data_str = match.group(1).replace('\\"', '"')
    
    # The data is nested, so we need to find the correct starting point
    json_start_str = '{"data":{"data":['
    start_index = json_data_str.find(json_start_str)
    if start_index == -1:
        print("Could not find the start of the JSON data within the captured string.")
        return
        
    # Find the end of the JSON data
    end_index = json_data_str.rfind(']}}') + 3
    json_data_str = json_data_str[start_index:end_index]

    try:
        data = json.loads(json_data_str)
        states_data = data['data']['data']
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing JSON data: {e}")
        return

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['State', 'Branch', 'Address', 'Latitude', 'Longitude'])

        for state_info in states_data:
            state_name = state_info.get('States', 'NA')
            branches = state_info.get('Branches', [])
            
            for branch_container in branches:
                branch_details = branch_container.get('BranchName', {})
                
                branch_name = branch_details.get('Branches', 'NA')
                address = branch_details.get('Address', 'NA')
                latitude = branch_details.get('Latitude', 'NA')
                longitude = branch_details.get('Longitude', 'NA')
                
                writer.writerow([state_name, branch_name, address, latitude, longitude])

if __name__ == '__main__':
    extract_shubham_data('shubham.html', 'shubham_branches.csv')
    print("Data extracted successfully to shubham_branches.csv")
