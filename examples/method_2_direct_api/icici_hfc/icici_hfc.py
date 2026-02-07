import requests

url = "https://www.icicihfc.com/bin/branchlocator?contentRequired=details&branch=Kakinada"

payload = {}
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Referer': 'https://www.icicihfc.com/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

states = ["Andhra Pradesh", "Bihar", "Chandigarh", "Chhattisgarh", "Delhi", "Gujarat", "Haryana", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "New Delhi", "Odisha", "Puducherry", "Punjab", "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh", "Uttarakhand", "West Bengal"]

andra_pradesh_cities= ["Bhimavaram", "Eluru", "Guntur", "Kakinada", "Kurnool", "Machilipatnam", "Nellore", "Ongole", "Rajahmundry", "Tirupati", "Vijayawada", "Visakhapatnam", "Vizianagaram"]
bihar_cities=["Patna"]
chandigarh_cities =["Chandigarh"]
chhattisgarh= ["Bilaspur", "Durg", "Raipur", "Raipur - Bhatagaon"]
Delhi_city=["Central Delhi - Karol Bagh", "Delhi - Model Town", "East Delhi - Laxmi Nagar", "North Delhi – Pitampura", "West Delhi – Janakpuri"]
gujurat_city=["Ahmedabad - Nikol", "Ahmedabad - SG Highway", "Ahmedabad - West", "Anand", "Bharuch", "Bhavnagar", "Bopal", "Chandkheda", "Gandhidham", "Himmatnagar", "Junagadh", "Mehsana", "Modasa", "Morbi", "Narol", "Palanpur", "Patan", "Rajkot", "Surat", "Vadodara", "Vadodara-Waghodia Road", "Vapi"]
haryana= ["Ambala", "Faridabad", "Gurgaon 1 - Sec 29", "Gurgaon – Sohna Road", "Hissar", "Karnal", "Panchkula", "Panipat", "Rohtak", "Sonipat", "Yamunanagar"]
jharkhand_city=["Jamshedpur", "Ranchi"]
karnataka_city=["Bangalore - J P Nagar", "Bangalore - JP Nagar (REL)", "Bangalore - Sahakar Nagar", "Bangalore - Yeshwantpur", "Bangalore-Koramangala", "Belgaum", "Bengaluru - Kalyan Nagar", "Bengaluru - Vijaynagar", "Davangere", "Gulbarga", "Hasan", "Hubli", "Kengeri", "Marathahalli", "Mysore", "Shimoga"]
Kerala_city=["Kochi", "Kollam", "Kottayam", "Kozhikode (Calicut)", "Palakkad", "Thiruvananthapuram (Trivandrum)", "Thrissur"]
Madhya_Pradesh_city= ["Ashta", "Bhopal", "Dewas", "Dhar", "Guna", "Gwalior", "Indore - Navlakha", "Indore - Phooti Kothi", "Indore - Vijaynagar", "Indore Main - MG road", "Jabalpur", "Mandsaur", "Pithampur", "Ratlam", "Sagar", "Satna", "Ujjain", "Vidisha"]
maharashtra= ["Ahmednagar", "Akola", "Amravati", "Andheri", "Aurangabad", "Badlapur", "Baramati", "Boisar", "Buldhana", "Chandrapur", "Chinchwad -Pune", "Dhule", "Dombivli", "Jalgaon", "Kalyan-Mumbai", "Kharadi", "Kolhapur", "Latur", "Mira Road", "Mumbai - Borivali", "Mumbai – CBD Belapur", "Mumbai- Malad West", "Nagpur", "Nagpur - CA Road", "Nagpur Wardha Road", "Nanded", "Nashik", "Nashik - Panchvati", "Nashik Road", "Panvel", "Pune - Baner", "Pune - Main", "Pune - Wakad", "Pune-Hadapsar", "Pune-Vishrantwadi", "Ratnagiri", "Sangli", "Satara", "Solapur", "Thane", "Vasai", "Vashi", "Virar"]
New_Delhi= ["Lajpat Nagar", "New Delhi- Dwarka"]
odisha= ["Bhubaneswar"]
Puducherry= ["Puducherry"]
punjab=["Amritsar", "Bhatinda", "Ferozpur", "Jalandhar", "Kharar", "Ludhiana", "Pathankot", "Patiala"]
Rajasthan=["Ajmer", "Alwar", "Balotra", "Beawar", "Bhilwara", "Bhiwadi", "Bikaner", "Chittorgarh", "Chomu", "Dausa", "Hanumangarh", "Jagatpura", "Jaipur", "Jaipur - Main", "Jaipur - Vaishali Nagar", "Jodhpur", "Kalwar road", "Kekri", "Kota", "Kotputli", "Pali", "Sikar", "SriGanganagar", "Tonk", "Udaipur", "Vidyadhar nagar"]
Tamil_Nadu=["Chennai - Annanagar", "Chennai - T Nagar", "Chennai - Tambaram", "Coimbatore", "Erode", "Hosur", "Madurai", "Nagercoil", "Salem", "Tenkasi", "Tirunelveli", "Tiruppur", "Trichy", "Tuticorin", "Vellore"]
Telangana =["Ameerpet", "Ameerpet NDMA", "ECIL Hyderabad", "Hyderabad - Dilsukhnagar", "Hyderabad - Kokapet", "Hyderabad - Kukatpally", "Hyderabad - Punjagutta", "Hyderabad - Secunderabad", "Hyderabad - Shamshabad", "Hyderabad – Kompally", "Khammam", "Nizamabad", "RC Puram", "Sangareddy", "Warangal"]
Uttar_Pradesh=["Agra", "Allahabad - Prayagraj", "Bareilly", "Bijnor", "Ghaziabad", "Gorakhpur", "Greater Noida", "Jankipuram", "Jhansi", "Kanpur", "Lucknow", "Lucknow- South", "Lucknow- Transportnagar", "Mathura", "Meerut", "Moradabad", "Noida", "Pilibhit", "Raebareli", "Saharanpur", "Varanasi"]
Uttarakhand= ["Central Dehradun", "Dehradun", "Dehradun-South", "Haldwani", "Haridwar", "Kashipur", "Roorkee", "Rudrapur", "Vikasnagar"]
West_Bengal=["Kolkata - AJC Bose Road", "Kolkata - Howrah", "Siliguri"]
