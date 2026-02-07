import requests
from bs4 import BeautifulSoup
import csv

def scrape_shivalik_branches():
    """
    Scrapes branch information from all pages of the Shivalik Bank website
    and saves it to a CSV file.
    """
    base_url = "https://shivalikbank.com/contact/branch"
    # Using the headers from your shivalik.py file
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://shivalikbank.com/contact/branch?page=2',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        # NOTE: Obtain fresh XSRF-TOKEN and sfsb_session by visiting https://shivalikbank.com/contact/branch
        'Cookie': 'XSRF-TOKEN=YOUR_XSRF_TOKEN; sfsb_session=YOUR_SESSION_TOKEN'
    }
    
    all_branches = []
    
    # Loop through pages 1 to 10
    for page_num in range(1, 11):
        params = {
            'page': page_num
        }
        
        print(f"Scraping page {page_num}...")
        
        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=15)
            response.raise_for_status() # Raise an exception for bad status codes
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            branch_containers = soup.find_all('div', class_='col-md-4')
            
            if not branch_containers:
                print(f"No more branches found on page {page_num}. Stopping.")
                break
                
            for branch in branch_containers:
                branch_name_tag = branch.find('h4')
                branch_name = branch_name_tag.text.strip() if branch_name_tag else 'NA'
                
                address_tag = branch.find('p')
                address = address_tag.text.strip() if address_tag else 'NA'
                
                if branch_name != 'NA':
                    all_branches.append({'Branch Name': branch_name, 'Address': address})

        except requests.exceptions.RequestException as e:
            print(f"Error scraping page {page_num}: {e}")
            continue

    output_file = 'shivalik_branches.csv'
    if not all_branches:
        print("No branches were scraped. CSV file will not be created.")
        return

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Branch Name', 'Address'])
        writer.writeheader()
        writer.writerows(all_branches)
        
    print(f"\nSuccessfully scraped {len(all_branches)} branches.")
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    scrape_shivalik_branches()