import requests

url = "https://apacfin.com/findPincode?id=177"

payload = {}
headers = {
  'accept': 'application/json, text/javascript, */*; q=0.01',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'cache-control': 'no-cache',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://apacfin.com/contact_us',
  'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
  'x-requested-with': 'XMLHttpRequest',
  # NOTE: Obtain fresh XSRF-TOKEN and apac_session by visiting https://apacfin.com/contact_us
  'Cookie': 'XSRF-TOKEN=YOUR_XSRF_TOKEN; apac_session=YOUR_SESSION_TOKEN'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

