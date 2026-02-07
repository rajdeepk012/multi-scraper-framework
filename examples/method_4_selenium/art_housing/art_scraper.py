from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import json
import time

# Set up Chrome options with performance logging
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the page to scrape
url = "https://arthfc.com/contact-details-statewise/"  # Replace with actual URL
driver.get(url)

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'bl-state-select')))

# List to store scraped data
data = []

# Function to safely click an element
def safe_click(element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)
        element.click()
        return True
    except Exception as e:
        try:
            driver.execute_script("arguments[0].click();", element)
            return True
        except:
            return False

# Function to get AJAX response from network logs
def get_ajax_response():
    logs = driver.get_log('performance')
    for log in logs:
        log_data = json.loads(log['message'])['message']
        if log_data['method'] == 'Network.responseReceived':
            url = log_data['params']['response']['url']
            if 'admin-ajax.php' in url:
                request_id = log_data['params']['requestId']
                try:
                    response = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                    if 'body' in response and response['body']:
                        # Try to parse as JSON
                        try:
                            return json.loads(response['body'])
                        except json.JSONDecodeError:
                            # If not JSON, return the raw body
                            return {'raw_body': response['body']}
                    else:
                        print("Empty response body")
                        return None
                except Exception as e:
                    print(f"Error getting response body: {e}")
                    return None
    return None

# Function to extract data from DOM as fallback
def extract_from_dom():
    try:
        # Wait for the branch details to be visible
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#bl-branch-details .branch-box'))
        )
        
        branch_box = driver.find_element(By.CSS_SELECTOR, '#bl-branch-details .branch-box')
        
        # Get branch name
        branch_title = branch_box.find_element(By.TAG_NAME, 'h4').text.strip()
        
        # Get address
        address_element = branch_box.find_element(By.CSS_SELECTOR, 'p.max-w80')
        address = address_element.text.strip()
        
        return {
            'title': branch_title,
            'address': address
        }
    except Exception as e:
        print(f"Error extracting from DOM: {e}")
        return None

# Get all state options first
state_dropdown = driver.find_element(By.CSS_SELECTOR, '.nice-select')
safe_click(state_dropdown)
state_options = driver.find_elements(By.CSS_SELECTOR, '.nice-select ul li.option')

# Store state information
states = []
for i in range(1, len(state_options)):
    state_option = state_options[i]
    state_name = state_option.text.strip()
    state_value = state_option.get_attribute('data-value')
    states.append({'name': state_name, 'value': state_value})

# Process each state
for state in states:
    state_name = state['name']
    state_value = state['value']
    
    print(f"Processing state: {state_name}")
    
    # Reopen the state dropdown
    state_dropdown = driver.find_element(By.CSS_SELECTOR, '.nice-select')
    safe_click(state_dropdown)
    
    # Find and click the state option
    state_options = driver.find_elements(By.CSS_SELECTOR, '.nice-select ul li.option')
    state_found = False
    for option in state_options:
        if option.get_attribute('data-value') == state_value:
            if safe_click(option):
                state_found = True
                break
    
    if not state_found:
        print(f"Could not find state: {state_name}")
        continue
    
    # Get the currently selected state name from the dropdown
    try:
        current_state_element = driver.find_element(By.CSS_SELECTOR, '.nice-select .current')
        current_state_name = current_state_element.text.strip()
        print(f"Current state selected: {current_state_name}")
    except Exception as e:
        print(f"Error getting current state: {e}")
        current_state_name = state_name  # Fallback to stored name
    
    # Wait for the branch dropdown to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'bl-branch-select')))
    except:
        print(f"Branch dropdown not found for state: {current_state_name}")
        continue
    
    # Get all branch options
    branch_select = driver.find_element(By.ID, 'bl-branch-select')
    branch_options = branch_select.find_elements(By.TAG_NAME, 'option')
    
    # Store branch information
    branches = []
    for j in range(1, len(branch_options)):
        branch_option = branch_options[j]
        branch_name = branch_option.text.strip()
        branch_value = branch_option.get_attribute('value')
        branches.append({'name': branch_name, 'value': branch_value})
    
    # Process each branch
    for branch in branches:
        branch_name = branch['name']
        branch_value = branch['value']
        
        print(f"  Processing branch: {branch_name}")
        
        # Select the branch
        branch_select = driver.find_element(By.ID, 'bl-branch-select')
        select = Select(branch_select)
        select.select_by_value(branch_value)
        
        # Wait for AJAX response
        time.sleep(1)
        
        # Try to get AJAX response
        ajax_response = get_ajax_response()
        
        # Initialize variables
        address = ''
        title = ''
        
        if ajax_response:
            try:
                # Check if response is in expected format
                if 'raw_body' in ajax_response:
                    # Handle non-JSON response
                    print(f"    Non-JSON response: {ajax_response['raw_body'][:100]}...")
                    # Try DOM extraction as fallback
                    dom_data = extract_from_dom()
                    if dom_data:
                        address = dom_data.get('address', '')
                        title = dom_data.get('title', '')
                else:
                    # Extract data from JSON response
                    address = ajax_response.get('address', '')
                    title = ajax_response.get('title', '')
                    
                    # If address or title is missing, try DOM extraction
                    if not address or not title:
                        dom_data = extract_from_dom()
                        if dom_data:
                            address = dom_data.get('address', address)
                            title = dom_data.get('title', title)
            except Exception as e:
                print(f"    Error extracting details from AJAX: {e}")
                # Try DOM extraction as fallback
                dom_data = extract_from_dom()
                if dom_data:
                    address = dom_data.get('address', '')
                    title = dom_data.get('title', '')
        else:
            print(f"    No AJAX response for {branch_name}, trying DOM extraction")
            # Try DOM extraction as fallback
            dom_data = extract_from_dom()
            if dom_data:
                address = dom_data.get('address', '')
                title = dom_data.get('title', '')
        
        # Add to data list if we have at least some data
        if address or title:
            data.append([current_state_name, branch_name, title, address])
            print(f"    Added: {current_state_name}, {branch_name}, {address[:50]}...")
        else:
            print(f"    No data extracted for {branch_name}")

# Write data to CSV file
with open('art_branches.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='@')
    writer.writerow(['State', 'City', 'Branch', 'Address'])
    writer.writerows(data)

print(f"Scraping complete. {len(data)} records saved to art_branches.csv")

# Close the WebDriver
driver.quit()