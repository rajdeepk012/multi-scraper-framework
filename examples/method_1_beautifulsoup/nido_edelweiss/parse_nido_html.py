from bs4 import BeautifulSoup
import csv
import re

def get_state_from_text(text_block):
    states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
        "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
        "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
        "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh",
        "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh",
        "Lakshadweep", "Pondicherry"
    ]
    for state in states:
        if re.search(r'\b' + re.escape(state) + r'\b', text_block, re.IGNORECASE):
            return state
    return "NA"

def parse_unico_html(html_file, csv_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find the container for all branch locations
    locations_container = soup.find('div', class_='branch-locations')
    if not locations_container:
        print("Error: Could not find the main branch locations container.")
        return

    # Find all individual location blocks
    locations = locations_container.find_all('div', class_='locations')

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='@')
        writer.writerow(["State", "City", "Address"])

        for loc in locations:
            city_tag = loc.find('h3')
            address_tag = loc.find('span', id=lambda x: x and x.startswith('rptLocation_lblAddress_'))

            if city_tag and address_tag:
                city = city_tag.get_text(strip=True)
                address = address_tag.get_text(strip=True).replace('\n', ' ')
                state = get_state_from_text(address)
                
                writer.writerow([state, city, address])

if __name__ == "__main__":
    html_file_path = 'unico.html'
    csv_file_path = 'unico_html_branches.csv'
    parse_unico_html(html_file_path, csv_file_path)
    print(f"Successfully parsed {html_file_path} and created {csv_file_path}")
