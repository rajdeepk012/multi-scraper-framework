import requests
import csv
import json

def scrape_icici_hfc_data():
    """Scrapes ICICI HFC branch data by hitting their API endpoint for each city."""
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }

    # Data provided by the user
    locations = {
        "Andhra Pradesh": ["Bhimavaram", "Eluru", "Guntur", "Kakinada", "Kurnool", "Machilipatnam", "Nellore", "Ongole", "Rajahmundry", "Tirupati", "Vijayawada", "Visakhapatnam", "Vizianagaram"],
        "Bihar": ["Patna"],
        "Chandigarh": ["Chandigarh"],
        "Chhattisgarh": ["Bilaspur", "Durg", "Raipur", "Raipur - Bhatagaon"],
        "Delhi": ["Central Delhi - Karol Bagh", "Delhi - Model Town", "East Delhi - Laxmi Nagar", "North Delhi – Pitampura", "West Delhi – Janakpuri"],
        "Gujarat": ["Ahmedabad - Nikol", "Ahmedabad - SG Highway", "Ahmedabad - West", "Anand", "Bharuch", "Bhavnagar", "Bopal", "Chandkheda", "Gandhidham", "Himmatnagar", "Junagadh", "Mehsana", "Modasa", "Morbi", "Narol", "Palanpur", "Patan", "Rajkot", "Surat", "Vadodara", "Vadodara-Waghodia Road", "Vapi"],
        "Haryana": ["Ambala", "Faridabad", "Gurgaon 1 - Sec 29", "Gurgaon – Sohna Road", "Hissar", "Karnal", "Panchkula", "Panipat", "Rohtak", "Sonipat", "Yamunanagar"],
        "Jharkhand": ["Jamshedpur", "Ranchi"],
        "Karnataka": ["Bangalore - J P Nagar", "Bangalore - JP Nagar (REL)", "Bangalore - Sahakar Nagar", "Bangalore - Yeshwantpur", "Bangalore-Koramangala", "Belgaum", "Bengaluru - Kalyan Nagar", "Bengaluru - Vijaynagar", "Davangere", "Gulbarga", "Hasan", "Hubli", "Kengeri", "Marathahalli", "Mysore", "Shimoga"],
        "Kerala": ["Kochi", "Kollam", "Kottayam", "Kozhikode (Calicut)", "Palakkad", "Thiruvananthapuram (Trivandrum)", "Thrissur"],
        "Madhya Pradesh": ["Ashta", "Bhopal", "Dewas", "Dhar", "Guna", "Gwalior", "Indore - Navlakha", "Indore - Phooti Kothi", "Indore - Vijaynagar", "Indore Main - MG road", "Jabalpur", "Mandsaur", "Pithampur", "Ratlam", "Sagar", "Satna", "Ujjain", "Vidisha"],
        "Maharashtra": ["Ahmednagar", "Akola", "Amravati", "Andheri", "Aurangabad", "Badlapur", "Baramati", "Boisar", "Buldhana", "Chandrapur", "Chinchwad - Pune", "Dhule", "Dombivli", "Jalgaon", "Kalyan-Mumbai", "Kharadi", "Kolhapur", "Latur", "Mira Road", "Mumbai - Borivali", "Mumbai – CBD Belapur", "Mumbai- Malad West", "Nagpur", "Nagpur - CA Road", "Nagpur Wardha Road", "Nanded", "Nashik", "Nashik - Panchvati", "Nashik Road", "Panvel", "Pune - Baner", "Pune - Main", "Pune - Wakad", "Pune-Hadapsar", "Pune-Vishrantwadi", "Ratnagiri", "Sangli", "Satara", "Solapur", "Thane", "Vasai", "Vashi", "Virar"],
        "New Delhi": ["Lajpat Nagar", "New Delhi- Dwarka"],
        "Odisha": ["Bhubaneswar"],
        "Puducherry": ["Puducherry"],
        "Punjab": ["Amritsar", "Bhatinda", "Ferozpur", "Jalandhar", "Kharar", "Ludhiana", "Pathankot", "Patiala"],
        "Rajasthan": ["Ajmer", "Alwar", "Balotra", "Beawar", "Bhilwara", "Bhiwadi", "Bikaner", "Chittorgarh", "Chomu", "Dausa", "Hanumangarh", "Jagatpura", "Jaipur", "Jaipur - Main", "Jaipur - Vaishali Nagar", "Jodhpur", "Kalwar road", "Kekri", "Kota", "Kotputli", "Pali", "Sikar", "SriGanganagar", "Tonk", "Udaipur", "Vidyadhar nagar"],
        "Tamil Nadu": ["Chennai - Annanagar", "Chennai - T Nagar", "Chennai - Tambaram", "Coimbatore", "Erode", "Hosur", "Madurai", "Nagercoil", "Salem", "Tenkasi", "Tirunelveli", "Tiruppur", "Trichy", "Tuticorin", "Vellore"],
        "Telangana": ["Ameerpet", "Ameerpet NDMA", "ECIL Hyderabad", "Hyderabad - Dilsukhnagar", "Hyderabad - Kokapet", "Hyderabad - Kukatpally", "Hyderabad - Punjagutta", "Hyderabad - Secunderabad", "Hyderabad - Shamshabad", "Hyderabad – Kompally", "Khammam", "Nizamabad", "RC Puram", "Sangareddy", "Warangal"],
        "Uttar Pradesh": ["Agra", "Allahabad - Prayagraj", "Bareilly", "Bijnor", "Ghaziabad", "Gorakhpur", "Greater Noida", "Jankipuram", "Jhansi", "Kanpur", "Lucknow", "Lucknow- South", "Lucknow- Transportnagar", "Mathura", "Meerut", "Moradabad", "Noida", "Pilibhit", "Raebareli", "Saharanpur", "Varanasi"],
        "Uttarakhand": ["Central Dehradun", "Dehradun", "Dehradun-South", "Haldwani", "Haridwar", "Kashipur", "Roorkee", "Rudrapur", "Vikasnagar"],
        "West Bengal": ["Kolkata - AJC Bose Road", "Kolkata - Howrah", "Siliguri"]
    }

    all_branches = []
    base_url = "https://www.icicihfc.com/bin/branchlocator?contentRequired=details&branch="

    for state, cities in locations.items():
        for city in cities:
            print(f"Fetching data for {city}, {state}...")
            url = f"{base_url}{city.replace(' ', '%20')}"
            try:
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                data = response.json()
                if data:
                    # The API returns a list, we take the first element
                    branch_info = data[0]
                    address = branch_info.get('address', 'N/A')
                    all_branches.append([state, city, address])
                else:
                    print(f"No data found for {city}, {state}")
            except requests.exceptions.RequestException as e:
                print(f"Could not fetch data for {city}, {state}. Error: {e}")
            except json.JSONDecodeError:
                print(f"Could not decode JSON for {city}, {state}")

    return all_branches

def save_to_csv(data, filename="icici_hfc_branches.csv"):
    """Saves the scraped data to a CSV file with '@' as the delimiter."""
    if not data:
        print("No data was scraped. CSV file will not be created.")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='@')
        writer.writerow(['State', 'City', 'Address'])
        writer.writerows(data)
    print(f"Data successfully saved to {filename}")

if __name__ == "__main__":
    scraped_data = scrape_icici_hfc_data()
    save_to_csv(scraped_data)
