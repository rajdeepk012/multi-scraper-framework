
from bs4 import BeautifulSoup
import csv
import re

def extract_csl_finance_data(html_file, csv_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    accordion_items = soup.find_all('li', class_='s__7YWojd')

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['State', 'City', 'Branch', 'Address', 'Latitude', 'Longitude'])

        for item in accordion_items:
            state_tag = item.find('h3', class_=re.compile(r'srbjKeO'))
            state = state_tag.text.strip() if state_tag else 'NA'

            branch_blocks = item.find_all('div', class_='MJXUU')
            for block in branch_blocks:
                # Find all potential branch names in the block
                branch_name_tags = block.find_all('span', style='font-weight:700')
                
                for i, branch_name_tag in enumerate(branch_name_tags):
                    try:
                        branch_name = branch_name_tag.text.strip()
                        if not branch_name:
                            continue

                        # Find address elements between this branch name and the next one
                        start_node = branch_name_tag.find_parent('p')
                        address_nodes = []
                        current_node = start_node
                        while current_node:
                            # Determine the end node
                            end_node = branch_name_tags[i+1].find_parent('p') if i + 1 < len(branch_name_tags) else None
                            
                            if current_node == end_node:
                                break
                            
                            address_nodes.append(current_node)
                            current_node = current_node.find_next_sibling()

                        address_lines = [node.text.strip() for node in address_nodes if node.text.strip()]
                        full_address = ' '.join(address_lines)
                        
                        city = branch_name

                        lat, lon = 'NA', 'NA'
                        # Find the button within the scope of the current branch address
                        button_container = None
                        for node in address_nodes:
                            # The button is usually in a div that's a sibling to the address paragraphs
                            button_div = node.find_next_sibling('div', class_='F3Ebu')
                            if button_div:
                                button_container = button_div
                                break
                        
                        if button_container:
                            location_button = button_container.find('a', attrs={'data-hook': 'buttonViewer'})
                            if location_button and location_button.get('href'):
                                href = location_button['href']
                                match = re.search(r'q=([0-9\.\,]+)', href)
                                if match:
                                    coords = match.group(1).split(',')
                                    if len(coords) == 2:
                                        lat, lon = coords[0], coords[1]

                        writer.writerow([state, city, branch_name, full_address, lat, lon])
                    except Exception as e:
                        # This will catch errors on the last branch of each block, which is expected
                        pass

if __name__ == '__main__':
    extract_csl_finance_data('cslfinance.html', 'csl_finance_branches.csv')
    print("Data extracted successfully to csl_finance_branches.csv")
