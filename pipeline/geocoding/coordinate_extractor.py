#!/usr/bin/env python3
"""
Optimized Google Maps URL Coordinate Extractor
- Fixed regex patterns
- Concurrent processing for speed
- Incremental saves every 25 extractions
- Reduced delays since bot detection wasn't the issue
"""

import csv
import time
import random
import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse, parse_qs
import logging
import concurrent.futures
import threading
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OptimizedCoordinateExtractor:
    def __init__(self, max_workers=8):
        self.max_workers = max_workers
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        self.results_lock = threading.Lock()
        self.processed_count = 0
        self.success_count = 0

    def _create_session(self):
        """Create a requests session with retry strategy and realistic headers"""
        session = requests.Session()

        # Retry strategy for handling temporary failures
        retry_strategy = Retry(
            total=2,  # Reduced retries since regex was the issue
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set realistic headers with random user agent
        user_agent = random.choice(self.user_agents)
        session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        return session

    def expand_url(self, short_url, branch_name="Unknown"):
        """
        Expand a shortened Google Maps URL and extract coordinates
        Optimized version with minimal delays and improved error handling
        """
        if not short_url or short_url.strip() == 'NA':
            return {
                'branch_name': branch_name,
                'expanded_url': None,
                'latitude': None,
                'longitude': None,
                'success': False,
                'error': 'No URL provided'
            }

        session = self._create_session()

        try:
            # Small random delay to avoid being too aggressive
            time.sleep(random.uniform(0.5, 1.5))

            logger.debug(f"Expanding URL for {branch_name}: {short_url}")

            # Use HEAD request first (lighter and faster)
            response = session.head(
                short_url,
                allow_redirects=True,
                timeout=10  # Reduced timeout
            )

            expanded_url = response.url
            logger.debug(f"Expanded to: {expanded_url}")

            # Extract coordinates from the expanded URL
            coordinates = self._extract_coordinates(expanded_url)

            if coordinates['latitude'] and coordinates['longitude']:
                return {
                    'branch_name': branch_name,
                    'expanded_url': expanded_url,
                    'latitude': coordinates['latitude'],
                    'longitude': coordinates['longitude'],
                    'success': True,
                    'error': None
                }
            else:
                # Try GET request if HEAD didn't work
                logger.debug(f"HEAD request didn't yield coordinates for {branch_name}, trying GET...")
                response = session.get(
                    short_url,
                    allow_redirects=True,
                    timeout=10
                )
                expanded_url = response.url
                coordinates = self._extract_coordinates(expanded_url)

                if coordinates['latitude'] and coordinates['longitude']:
                    return {
                        'branch_name': branch_name,
                        'expanded_url': expanded_url,
                        'latitude': coordinates['latitude'],
                        'longitude': coordinates['longitude'],
                        'success': True,
                        'error': None
                    }

        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed for {branch_name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for {branch_name}: {e}")

        return {
            'branch_name': branch_name,
            'expanded_url': None,
            'latitude': None,
            'longitude': None,
            'success': False,
            'error': 'Failed to extract coordinates'
        }

    def _extract_coordinates(self, url):
        """Extract latitude and longitude from Google Maps URL patterns"""
        lat, lng = None, None

        # Pattern 1: @latitude,longitude format (FIXED REGEX)
        coord_pattern = r'@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)'
        match = re.search(coord_pattern, url)
        if match:
            lat, lng = float(match.group(1)), float(match.group(2))
            logger.debug(f"Extracted coordinates (pattern 1): {lat}, {lng}")
            return {'latitude': lat, 'longitude': lng}

        # Pattern 2: Query parameters
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Check for 'll' parameter
        if 'll' in query_params:
            coords = query_params['ll'][0].split(',')
            if len(coords) == 2:
                try:
                    lat, lng = float(coords[0]), float(coords[1])
                    logger.debug(f"Extracted coordinates (pattern 2): {lat}, {lng}")
                    return {'latitude': lat, 'longitude': lng}
                except ValueError:
                    pass

        # Pattern 3: Individual lat/lng parameters
        if 'lat' in query_params and 'lng' in query_params:
            try:
                lat = float(query_params['lat'][0])
                lng = float(query_params['lng'][0])
                logger.debug(f"Extracted coordinates (pattern 3): {lat}, {lng}")
                return {'latitude': lat, 'longitude': lng}
            except (ValueError, IndexError):
                pass

        # Pattern 4: Place patterns (FIXED REGEX)
        place_pattern = r'/(?:place/)?@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)(?:,\d+(?:\.\d+)?)?'
        match = re.search(place_pattern, url)
        if match:
            lat, lng = float(match.group(1)), float(match.group(2))
            logger.debug(f"Extracted coordinates (pattern 4): {lat}, {lng}")
            return {'latitude': lat, 'longitude': lng}

        logger.warning(f"Could not extract coordinates from URL: {url}")
        return {'latitude': None, 'longitude': None}

    def _save_incremental_results(self, results, output_file, batch_num):
        """Save results incrementally every 25 extractions"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{output_file.replace('.csv', '')}_backup_batch_{batch_num}_{timestamp}.csv"

        try:
            self._write_results_csv(results, backup_file)
            logger.info(f"💾 Incremental save: {len(results)} results saved to {backup_file}")
        except Exception as e:
            logger.error(f"Failed to save incremental backup: {e}")

    def _write_results_csv(self, results, output_file):
        """Write results to CSV file"""
        if not results:
            logger.error("No results to write")
            return

        fieldnames = [
            'Branch Name', 'Address', 'Google Maps Link', 'Expanded URL',
            'Latitude', 'Longitude', 'Extraction Success', 'Error'
        ]

        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    def process_csv_concurrent(self, input_file, output_file, save_interval=25):
        """
        Process CSV with concurrent URL expansion and incremental saves
        """
        results = []
        start_time = time.time()

        logger.info(f"🚀 Starting optimized processing of {input_file}")
        logger.info(f"💡 Using {self.max_workers} concurrent workers")
        logger.info(f"💾 Saving incremental backups every {save_interval} extractions")

        # Read the input CSV
        with open(input_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

        total_rows = len(rows)
        logger.info(f"📊 Found {total_rows} rows to process")

        # Process in concurrent batches
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_row = {}
            for i, row in enumerate(rows):
                branch_name = row.get('Branch Name', '').strip()
                google_maps_link = row.get('Google Maps Link', '').strip()

                future = executor.submit(self.expand_url, google_maps_link, branch_name)
                future_to_row[future] = (i, row)

            # Collect results as they complete
            batch_results = []
            batch_count = 0

            for future in concurrent.futures.as_completed(future_to_row):
                i, row = future_to_row[future]
                branch_name = row.get('Branch Name', '').strip()
                address = row.get('Address', '').strip()
                google_maps_link = row.get('Google Maps Link', '').strip()

                try:
                    result = future.result()

                    # Prepare result row
                    result_row = {
                        'Branch Name': branch_name,
                        'Address': address,
                        'Google Maps Link': google_maps_link,
                        'Expanded URL': result.get('expanded_url', ''),
                        'Latitude': result.get('latitude', ''),
                        'Longitude': result.get('longitude', ''),
                        'Extraction Success': result.get('success', False),
                        'Error': result.get('error', '')
                    }

                    with self.results_lock:
                        results.append(result_row)
                        batch_results.append(result_row)
                        self.processed_count += 1

                        if result['success']:
                            self.success_count += 1
                            logger.info(f"✅ [{self.processed_count}/{total_rows}] {branch_name} -> {result['latitude']}, {result['longitude']}")
                        else:
                            logger.warning(f"❌ [{self.processed_count}/{total_rows}] {branch_name} -> {result.get('error', 'Unknown error')}")

                        # Save incremental backup every save_interval
                        if len(batch_results) >= save_interval:
                            batch_count += 1
                            self._save_incremental_results(results.copy(), output_file, batch_count)
                            batch_results.clear()

                except Exception as e:
                    logger.error(f"Error processing {branch_name}: {e}")

        # Final save
        self._write_results_csv(results, output_file)

        # Calculate timing
        end_time = time.time()
        total_time = end_time - start_time

        # Print final summary
        logger.info(f"\n{'='*60}")
        logger.info(f"🎉 EXTRACTION COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"📊 Total processed: {self.processed_count}")
        logger.info(f"✅ Successful extractions: {self.success_count}")
        logger.info(f"❌ Failed extractions: {self.processed_count - self.success_count}")
        logger.info(f"📈 Success rate: {(self.success_count/self.processed_count)*100:.1f}%")
        logger.info(f"⏱️  Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        logger.info(f"🚀 Average speed: {self.processed_count/total_time:.1f} URLs/second")
        logger.info(f"💾 Results saved to: {output_file}")

        return results

def main():
    """Main function to run the optimized coordinate extraction"""
    input_file = '../samples/sample_input.csv'
    output_file = '../samples/sample_output.csv'

    # Create extractor with 8 concurrent workers (adjust based on your system)
    extractor = OptimizedCoordinateExtractor(max_workers=8)

    # Process the CSV file with concurrent processing and incremental saves
    results = extractor.process_csv_concurrent(
        input_file=input_file,
        output_file=output_file,
        save_interval=25  # Save every 25 extractions
    )

    print(f"\n🎉 Optimized coordinate extraction completed!")
    print(f"💾 Results saved to: {output_file}")

if __name__ == "__main__":
    main()