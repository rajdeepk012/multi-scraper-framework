import time
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def main():
    url = "https://protium.co.in/visit-us/"
    
    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Use a try-except block to ensure the browser is closed
    try:
        print("Setting up browser with automatic driver management...")
        # Use webdriver-manager to automatically download and manage the chromedriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        
        print(f"Fetching page with a headless browser: {url}")
        driver.get(url)
        
        # Wait for the table to be populated by JavaScript
        # A longer wait might be necessary for slower network conditions or complex scripts
        print("Waiting for page to render...")
        time.sleep(15)
        
        print("Page loaded. Parsing content...")
        # Get the page source after JavaScript has run
        page_source = driver.page_source

        # --- Diagnostic Step ---
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        print("Saved page source to debug_page_source.html for inspection.")
        # ----------------------

        soup = BeautifulSoup(page_source, 'html.parser')

        table = soup.find('table', {'id': 'tablepress-9'})
        if not table:
            print("Error: Could not find the data table with id 'tablepress-9'. The page structure might have changed.")
            return

        # Prepare the CSV file
        csv_file = 'protium_branches.csv'
        csv_headers = ['Branch Name', 'City', 'State/UT', 'Business Hours', 'Contact Number', 'Address', 'Latitude', 'Longitude', 'Location URL']
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='@', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(csv_headers)
            total_branches = 0

            while True:
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                table = soup.find('table', {'id': 'tablepress-9'})

                for row in table.find('tbody').find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) < 7:
                        continue

                    branch_name = cells[0].get_text(strip=True)
                    city = cells[1].get_text(strip=True)
                    state_ut = cells[2].get_text(strip=True)
                    business_hours = cells[3].get_text(strip=True)
                    contact_number = cells[4].get_text(strip=True)
                    address = cells[5].get_text(strip=True)
                    
                    lat, lon, gmaps_url = "N/A", "N/A", "N/A"
                    direction_link = cells[6].find('a')
                    if direction_link and direction_link.has_attr('href'):
                        gmaps_url = direction_link['href']
                        match = re.search(r'query=([0-9.-]+),([0-9.-]+)', gmaps_url)
                        if match:
                            lat = match.group(1)
                            lon = match.group(2)

                    writer.writerow([branch_name, city, state_ut, business_hours, contact_number, address, lat, lon, gmaps_url])
                    total_branches += 1
                
                try:
                    # Use a more robust XPath selector to find the button
                    next_button = driver.find_element(By.XPATH, '//button[contains(@class, "next") and not(contains(@class, "disabled"))]')
                    print("Clicking the 'Next' button...")
                    driver.execute_script("arguments[0].click();", next_button) # Use JavaScript click to be more reliable
                    time.sleep(2) # Wait for the next page to load
                except:
                    print("Could not find the 'Next' button or it is disabled. Assuming we are done.")
                    break

        print(f"\nExtraction complete. Total branches found: {total_branches}. File saved as: {csv_file}")

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()