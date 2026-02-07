
import json
import csv

def extract_indusind_data(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['State', 'City', 'Branch', 'Address', 'Latitude', 'Longitude'])

        for branch in data:
            state = branch.get('state', 'NA')
            city = branch.get('city', 'NA')
            branch_name = branch.get('locations', 'NA')
            address = branch.get('address', 'NA')
            latitude = branch.get('latitude', 'NA')
            longitude = branch.get('longitude', 'NA')

            writer.writerow([state, city, branch_name, address, latitude, longitude])

if __name__ == '__main__':
    # Corrected the file name to match the one provided in the prompt
    extract_indusind_data('indusind_branch.json', 'indusind_branches.csv')
    print("Data extracted successfully to indusind_branches.csv")
