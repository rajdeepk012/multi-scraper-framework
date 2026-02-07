from bs4 import BeautifulSoup
import csv
import os

def parse_all_shivalik_html():
    """
    Parses multiple locally saved Shivalik Bank HTML files (page1.html, etc.)
    and consolidates the branch information into a single CSV file with '@' delimiter.
    """
    all_branches = []
    
    # Loop through page numbers 1 to 10, as more might be added later
    for page_num in range(1, 11):
        file_path = f'page{page_num}.html'
        
        if not os.path.exists(file_path):
            # This is expected if not all pages were saved
            continue

        print(f"Parsing {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                if not html_content:
                    print(f"Warning: {file_path} is empty.")
                    continue
                soup = BeautifulSoup(html_content, 'html.parser')
        except Exception as e:
            print(f"Error reading or parsing {file_path}: {e}")
            continue

        branch_containers = soup.find_all('div', class_='col-lg-4')

        for branch in branch_containers:
            branch_name_tag = branch.find('h3')
            branch_name = branch_name_tag.text.strip() if branch_name_tag else 'NA'
            
            address_tag = branch.find('p', class_='branchatm_address')
            # Clean up the address text
            address = ' '.join(address_tag.text.split()) if address_tag else 'NA'
            
            if branch_name != 'NA' and address != 'NA':
                all_branches.append({'Branch Name': branch_name, 'Address': address})

    # Remove duplicates before writing to CSV
    unique_branches = []
    seen = set()
    for branch in all_branches:
        identifier = (branch['Branch Name'], branch['Address'])
        if identifier not in seen:
            unique_branches.append(branch)
            seen.add(identifier)

    output_file = 'shivalik_branches_all.csv'
    if not unique_branches:
        print("No branches were extracted from any of the HTML files.")
        return

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Branch Name', 'Address'], delimiter='@')
        writer.writeheader()
        writer.writerows(unique_branches)
        
    print(f"\nSuccessfully extracted a total of {len(unique_branches)} unique branches.")
    print(f"Consolidated data saved to {output_file}")

if __name__ == "__main__":
    parse_all_shivalik_html()
