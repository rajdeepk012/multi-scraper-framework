import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.saraswatbank.com/locator.aspx?id=LocateUs"
driver.get(url)

# Prepare CSV file
csv_file = open('sarswat_branches.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file, delimiter='@')
csv_writer.writerow(['State', 'City', 'Area', 'Address'])

try:
    # Wait for page to load
    wait = WebDriverWait(driver, 20)
    
    # Wait for state dropdown to load
    state_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlState")))
    
    # Get all state options (excluding "Select State")
    state_options = state_dropdown.find_elements(By.TAG_NAME, "option")[1:]
    print(f"Found {len(state_options)} states")
    
    for state_option in state_options:
        state_value = state_option.get_attribute("value")
        state_name = state_option.text
        print(f"Processing state: {state_name}")
        
        # Select state
        state_dropdown.click()
        state_option.click()
        
        # Wait for city dropdown to update and get options
        city_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlCity")))
        time.sleep(1)  # Allow time for city dropdown to populate
        
        city_options = city_dropdown.find_elements(By.TAG_NAME, "option")[1:]
        print(f"Found {len(city_options)} cities in {state_name}")
        
        for city_option in city_options:
            city_value = city_option.get_attribute("value")
            city_name = city_option.text
            print(f"Processing city: {city_name}")
            
            # Select city
            city_dropdown.click()
            city_option.click()
            
            # Wait for area dropdown to update and get options
            area_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlArea")))
            time.sleep(1)  # Allow time for area dropdown to populate
            
            area_options = area_dropdown.find_elements(By.TAG_NAME, "option")[1:]
            print(f"Found {len(area_options)} areas in {city_name}")
            
            for area_option in area_options:
                area_value = area_option.get_attribute("value")
                area_name = area_option.text
                print(f"Processing area: {area_name}")
                
                # Select area
                area_dropdown.click()
                area_option.click()
                time.sleep(1)
                
                # Click submit button
                submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='button'][value='Submit']")
                driver.execute_script("arguments[0].click();", submit_button)
                
                # Wait for branch details to appear and stabilize
                try:
                    # First, wait for the branch details element to be present
                    branch_details = wait.until(
                        EC.presence_of_element_located((By.ID, "branchDetails"))
                    )
                    
                    # Then wait for it to be visible (not hidden)
                    wait.until(
                        EC.visibility_of_element_located((By.ID, "branchDetails"))
                    )
                    
                    # Additional wait to ensure content is loaded
                    time.sleep(2)
                    
                    # Check if the branch details section has content
                    if branch_details.text.strip() == "":
                        print(f"No branch details content for {state_name}, {city_name}, {area_name}")
                        address = "N/A"
                    else:
                        # Extract address using multiple methods
                        address = "N/A"
                        
                        # Method 1: Try to find address element by XPath
                        try:
                            address_element = branch_details.find_element(By.XPATH, ".//li[span[text()='Address']]")
                            address = address_element.text.replace("Address", "").strip()
                            if address:
                                print(f"Found address (method 1): {address}")
                        except:
                            pass
                        
                        # Method 2: If method 1 failed, try to find by CSS selector
                        if address == "N/A":
                            try:
                                address_element = branch_details.find_element(By.CSS_SELECTOR, "li:has(span:contains('Address'))")
                                # Get the text of the li element and remove the span part
                                address = address_element.text.replace("Address", "").strip()
                                if address:
                                    print(f"Found address (method 2): {address}")
                            except:
                                pass
                        
                        # Method 3: If methods 1 and 2 failed, try to extract from the entire HTML
                        if address == "N/A":
                            try:
                                # Get the HTML of the branch details
                                branch_html = branch_details.get_attribute('innerHTML')
                                
                                # Use regex to extract address
                                address_match = re.search(r'<li>\s*<span>Address</span>(.*?)</li>', branch_html, re.DOTALL)
                                if address_match:
                                    address = address_match.group(1).strip()
                                    # Remove any HTML tags
                                    address = re.sub(r'<[^>]+>', '', address)
                                    if address:
                                        print(f"Found address (method 3): {address}")
                            except:
                                pass
                        
                        # Method 4: If all else failed, try to find any list item containing "Address"
                        if address == "N/A":
                            try:
                                list_items = branch_details.find_elements(By.TAG_NAME, "li")
                                for item in list_items:
                                    if "Address" in item.text:
                                        # Split by "Address" and take the second part
                                        parts = item.text.split("Address", 1)
                                        if len(parts) > 1:
                                            address = parts[1].strip()
                                            if address:
                                                print(f"Found address (method 4): {address}")
                                                break
                            except:
                                pass
                        
                        # If we still don't have an address, get the entire text of branch_details
                        if address == "N/A":
                            print(f"Branch details text: {branch_details.text}")
                            print(f"Branch details HTML: {branch_details.get_attribute('innerHTML')}")
                    
                    # Write to CSV
                    csv_writer.writerow([state_name, city_name, area_name, address])
                    print(f"Saved to CSV: {state_name}, {city_name}, {area_name}, {address}")
                    
                except Exception as e:
                    print(f"No branch details found for {state_name}, {city_name}, {area_name}: {str(e)}")
                    continue
                
                # Reset area dropdown for next iteration
                area_dropdown = driver.find_element(By.ID, "ddlArea")
                area_dropdown.click()
                driver.find_element(By.CSS_SELECTOR, "#ddlArea option[value='-1']").click()
                time.sleep(0.5)
                
                # Clear branch details to avoid mixing data
                driver.execute_script("document.getElementById('branchDetails').innerHTML = '';")
                time.sleep(0.5)
            
            # Reset city dropdown for next iteration
            city_dropdown = driver.find_element(By.ID, "ddlCity")
            city_dropdown.click()
            driver.find_element(By.CSS_SELECTOR, "#ddlCity option[value='-1']").click()
            time.sleep(0.5)
        
        # Reset state dropdown for next iteration
        state_dropdown = driver.find_element(By.ID, "ddlState")
        state_dropdown.click()
        driver.find_element(By.CSS_SELECTOR, "#ddlState option[value='-1']").click()
        time.sleep(0.5)

finally:
    # Clean up
    csv_file.close()
    driver.quit()
    print("Scraping completed. Data saved to sarswat_branches.csv")