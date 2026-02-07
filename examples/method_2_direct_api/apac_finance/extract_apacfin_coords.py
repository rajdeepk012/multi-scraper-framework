import csv
import pandas as pd
import time
import logging
import requests
import re
from urllib.parse import urlparse, parse_qs
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AggressiveCoordinateExtractor:
    def __init__(self, max_workers=2):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        ]

    def _create_session(self):
        session = requests.Session()
        session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
        })
        return session

    def expand_url_aggressive(self, short_url, branch_name="Unknown"):
        if not short_url or not isinstance(short_url, str) or short_url.strip() == 'NA':
            return {
                'branch_name': branch_name,
                'expanded_url': None,
                'latitude': None,
                'longitude': None,
                'success': False,
                'error': 'No URL provided'
            }

        session = self._create_session()

        for attempt in range(3):
            try:
                time.sleep(random.uniform(1, 3))
                user_agent = random.choice(self.user_agents)
                session.headers.update({'User-Agent': user_agent})
                logger.info(f"Attempt {attempt+1} for {branch_name} with URL {short_url}")

                response = session.get(short_url, allow_redirects=True, timeout=15)
                expanded_url = response.url
                logger.debug(f"Expanded to: {expanded_url}")

                coordinates = self._extract_coordinates_aggressive(expanded_url, response.text)

                if coordinates['latitude'] and coordinates['longitude']:
                    logger.info(f"✅ Success for {branch_name}: {coordinates['latitude']}, {coordinates['longitude']}")
                    return {
                        'branch_name': branch_name,
                        'expanded_url': expanded_url,
                        'latitude': coordinates['latitude'],
                        'longitude': coordinates['longitude'],
                        'success': True,
                        'error': None
                    }

            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed for {branch_name}: {e}")
                if attempt < 2:
                    time.sleep(random.uniform(2, 5))

        logger.warning(f"❌ All attempts failed for {branch_name}")
        return {
            'branch_name': branch_name,
            'expanded_url': None,
            'latitude': None,
            'longitude': None,
            'success': False,
            'error': 'Failed after aggressive retry'
        }

    def _extract_coordinates_aggressive(self, url, response_text=None):
        lat, lng = None, None
        # New pattern for embed HTML content
        if response_text:
            # This pattern looks for the typical way coordinates are stored in Google embed page source
            match = re.search(r'!1d(-?\d+\.\d+)!2d(-?\d+\.\d+)', response_text)
            if match:
                try:
                    # Note the order is different in the pb string: lng, lat
                    lng, lat = float(match.group(1)), float(match.group(2))
                    return {'latitude': lat, 'longitude': lng}
                except (ValueError, IndexError):
                    pass

        # Fallback to original URL patterns if text search fails
        patterns = [
            r'@(-?\d+\.\d+),(-?\d+\.\d+)',
            r'!3d(-?\d+\.\d+)&!4d(-?\d+\.\d+)',
            r'center=(-?\d+\.\d+)%2C(-?\d+\.\d+)',
            r'll=(-?\d+\.\d+)%2C(-?\d+\.\d+)',
        ]

        for i, pattern in enumerate(patterns):
            match = re.search(pattern, url)
            if match:
                try:
                    lat, lng = float(match.group(1)), float(match.group(2))
                    return {'latitude': lat, 'longitude': lng}
                except (ValueError, IndexError):
                    continue

        return {'latitude': None, 'longitude': None}

def test_apacfin_extraction():
    try:
        df = pd.read_csv('apacfin_branches.csv')
    except FileNotFoundError:
        logger.error("Input file 'apacfin_branches.csv' not found.")
        return

    test_df = df.head(5)
    extractor = AggressiveCoordinateExtractor()

    print("--- Starting Extraction Test for first 5 APACFIN links ---")

    for index, row in test_df.iterrows():
        branch_name = row['City/Branch']
        map_link = row['Embedded Map Link']
        
        print("\n--------------------------------------------------")
        print(f"Processing Branch: {branch_name}")
        print(f"Original URL: {map_link}")

        result = extractor.expand_url_aggressive(map_link, branch_name)

        if result['success']:
            print(f"  \033[92mSUCCESS\033[0m")
            print(f"  Expanded URL: {result['expanded_url']}")
            print(f"  Latitude: {result['latitude']}")
            print(f"  Longitude: {result['longitude']}")
        else:
            print(f"  \033[91mFAILURE\033[0m")
            print(f"  Error: {result.get('error', 'Could not extract coordinates')}")
    
    print("\n--- Test Complete ---")

if __name__ == "__main__":
    test_apacfin_extraction()