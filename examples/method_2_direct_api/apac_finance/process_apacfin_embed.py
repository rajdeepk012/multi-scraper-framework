#!/usr/bin/env python3
"""
APAC Finance Embedded URL Coordinate Extractor
Extracts coordinates directly from Google Maps embed URLs (no HTTP requests needed!)
"""

import csv
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmbedURLCoordinateExtractor:
    def __init__(self):
        # Patterns for Google Maps embed URLs
        self.embed_patterns = [
            r'!2d(-?\d+(?:\.\d+)?).*?!3d(-?\d+(?:\.\d+)?)',  # !2d=longitude, !3d=latitude (most common)
            r'!3d(-?\d+(?:\.\d+)?).*?!4d(-?\d+(?:\.\d+)?)',  # !3d=latitude, !4d=longitude (alternate)
        ]

    def extract_from_embed_url(self, url):
        """
        Extract coordinates directly from Google Maps embed URL
        Returns: (latitude, longitude) or (None, None)
        """
        if not url or not isinstance(url, str) or url.strip() in ['NA', '#', '']:
            return None, None

        # Try each pattern
        for i, pattern in enumerate(self.embed_patterns):
            match = re.search(pattern, url)
            if match:
                if i == 0:  # !2d (lng) !3d (lat)
                    lng, lat = match.groups()
                else:  # !3d (lat) !4d (lng)
                    lat, lng = match.groups()

                try:
                    lat_float = float(lat)
                    lng_float = float(lng)

                    # Validate coordinates are in reasonable range for India
                    if 6 <= lat_float <= 37 and 68 <= lng_float <= 97:
                        return lat_float, lng_float
                    else:
                        logger.warning(f"Coordinates out of India range: {lat_float}, {lng_float}")
                        return None, None

                except (ValueError, TypeError):
                    continue

        return None, None

    def process_csv(self, input_file, output_file):
        """Process APAC Finance CSV and extract coordinates from embed URLs"""
        results = []
        success_count = 0
        failed_count = 0

        logger.info(f"🚀 Starting APAC Finance embed URL processing")
        logger.info(f"📂 Input file: {input_file}")

        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                rows = list(csv_reader)
        except FileNotFoundError:
            logger.error(f"Input file not found: {input_file}")
            return

        total_rows = len(rows)
        logger.info(f"📊 Found {total_rows} branches to process")
        logger.info(f"💡 Processing instant (no HTTP requests needed!)")
        print()

        for i, row in enumerate(rows, 1):
            branch_name = row.get('City/Branch', f'Row_{i}').strip()
            embed_url = row.get('Embedded Map Link', '').strip()

            # Extract coordinates
            lat, lng = self.extract_from_embed_url(embed_url)

            # Update row with results
            row.update({
                'Latitude': lat if lat else '',
                'Longitude': lng if lng else '',
                'Extraction Success': bool(lat and lng),
                'Error': '' if lat and lng else ('No URL' if not embed_url else 'Failed to parse')
            })

            results.append(row)

            if lat and lng:
                success_count += 1
                logger.info(f"✅ [{i}/{total_rows}] {branch_name} -> {lat}, {lng}")
            else:
                failed_count += 1
                error = 'No URL provided' if not embed_url else 'Failed to parse coordinates'
                logger.warning(f"❌ [{i}/{total_rows}] {branch_name} -> {error}")

        # Save results
        if results:
            original_fieldnames = list(rows[0].keys()) if rows else []
            new_fieldnames = ['Latitude', 'Longitude', 'Extraction Success', 'Error']
            final_fieldnames = [f for f in original_fieldnames if f not in new_fieldnames] + new_fieldnames

            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=final_fieldnames)
                writer.writeheader()
                writer.writerows(results)

        # Print summary
        print()
        logger.info(f"{'='*60}")
        logger.info(f"🎉 APAC FINANCE EXTRACTION COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"📊 Total processed: {total_rows}")
        logger.info(f"✅ Successful extractions: {success_count}")
        logger.info(f"❌ Failed extractions: {failed_count}")
        logger.info(f"📈 Success rate: {(success_count/total_rows)*100:.1f}%")
        logger.info(f"💾 Results saved to: {output_file}")
        logger.info(f"{'='*60}")

        return results

def main():
    """Main function to process APAC Finance embedded URLs"""
    input_file = 'apacfin_branches.csv'
    output_file = 'apacfin_branches_with_coords.csv'

    extractor = EmbedURLCoordinateExtractor()
    extractor.process_csv(input_file, output_file)

if __name__ == "__main__":
    main()
