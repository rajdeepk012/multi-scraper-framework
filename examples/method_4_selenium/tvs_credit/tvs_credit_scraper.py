
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        url = "https://www.tvscredit.com/branch-locator/"
        print(f"Navigating to {url}")
        driver.get(url)

        # Wait for the state dropdown to be populated
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "state")))
        
        state_dropdown = Select(driver.find_element(By.ID, "state"))
        # Get all state options except the first one which is a placeholder
        state_options = [option.get_attribute('value') for option in state_dropdown.options if option.get_attribute('value')]

        print(f"Found {len(state_options)} states to scrape.")
        
        all_branches = []
        
        for state_value in state_options:
            try:
                # Re-locate the dropdowns in each iteration to avoid stale element reference
                state_dropdown = Select(driver.find_element(By.ID, "state"))
                state_dropdown.select_by_value(state_value)
                print(f"\nScraping state: {state_value}")

                # Wait for the city dropdown to be populated for the selected state
                time.sleep(2) # A small static wait can be helpful here

                city_dropdown = Select(driver.find_element(By.ID, "city"))
                city_options = [option.get_attribute('value') for option in city_dropdown.options if option.get_attribute('value')]

                if not city_options:
                    print(f"  No cities found for {state_value}.")
                    continue

                for city_value in city_options:
                    try:
                        city_dropdown = Select(driver.find_element(By.ID, "city"))
                        city_dropdown.select_by_value(city_value)
                        print(f"  - Scraping city: {city_value}")

                        # Trigger the search/filter
                        driver.find_element(By.ID, "branch-search").click()
                        
                        # Wait for the branch details to appear
                        time.sleep(2)

                        # Find all branch cards
                        branch_cards = driver.find_elements(By.CLASS_NAME, "branch-info")
                        if not branch_cards:
                            print("    No branch info cards found for this city.")
                            continue
                            
                        for card in branch_cards:
                            try:
                                address = card.find_element(By.TAG_NAME, "p").text.strip()
                                # The "Get Directions" link contains the coordinates
                                directions_link = card.find_element(By.TAG_NAME, "a").get_attribute('href')
                                
                                lat, lon = "N/A", "N/A"
                                if directions_link and "maps.google.com" in directions_link:
                                    # Extract lat/lon from the google maps link
                                    query_params = directions_link.split('?')[1]
                                    for param in query_params.split('&'):
                                        if 'q=' in param:
                                            coords = param.replace('q=', '').split(',')
                                            if len(coords) == 2:
                                                lat, lon = coords[0], coords[1]
                                            break
                                
                                all_branches.append({
                                    "State": state_value,
                                    "City": city_value,
                                    "Address": address,
                                    "Latitude": lat,
                                    "Longitude": lon,
                                    "Google_Maps_URL": directions_link
                                })
                            except NoSuchElementException:
                                print("    Could not extract details from a branch card.")
                                continue

                    except (NoSuchElementException, TimeoutException) as e:
                        print(f"    Could not process city {city_value}. Error: {e}")
                        continue
            
            except (NoSuchElementException, TimeoutException) as e:
                print(f"  Could not process state {state_value}. Error: {e}")
                continue

        # Save to CSV
        csv_file = 'tvs_credit_branches.csv'
        csv_headers = ["State", "City", "Address", "Latitude", "Longitude", "Google_Maps_URL"]
        print(f"\nWriting {len(all_branches)} branches to {csv_file}...")
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            writer.writerows(all_branches)
        print("Scraping complete.")

    finally:
        print("Closing browser.")
        driver.quit()

if __name__ == "__main__":
    main()
