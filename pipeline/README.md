# Pipeline Utilities

Post-scraping tools for enriching, validating, and deduplicating branch data.

## Overview

After scraping raw branch data, these utilities handle the downstream processing:

```
Raw CSV → Geocoding → Validation → Deduplication → Final Output
```

## Geocoding

### `geocoding/coordinate_extractor.py`
Expands shortened Google Maps URLs (goo.gl, maps.app.goo.gl) to extract latitude/longitude coordinates.

- **Concurrent processing** with 8 workers for speed
- **Incremental saves** every 25 extractions (crash-safe)
- **4 regex patterns** for different Google Maps URL formats
- **HEAD-then-GET** strategy: tries lightweight HEAD request first, falls back to full GET

```bash
# Usage: Update input/output paths in main(), then run
python geocoding/coordinate_extractor.py
```

### `geocoding/address_geocoder.py`
Uses Google Geocoding API to enrich addresses with pincode, city, state, and coordinates.

- Requires `GOOGLE_GEOCODE_API_KEY` in `.env` file
- 50ms rate limiting between requests
- Extracts: formatted address, pincode, city, state, lat, lng

```bash
# Setup: Create .env with your API key (see .env.example in repo root)
python geocoding/address_geocoder.py
```

## Validation

### `validation/compare_by_pincode.py`
Matches branch records between existing data and newly scraped data using 6-digit pincodes.

- Regex-based pincode extraction: `\b(\d{6})\b`
- Inner merge produces side-by-side address comparison
- Output: Excel file with matching pincodes and both addresses

### `validation/find_duplicates.py`
Identifies and removes duplicate branch records.

- **Address normalization**: lowercase, remove punctuation, extract pincode
- **Match key**: normalized address + pincode combination
- **Set-based lookup**: O(1) duplicate detection
- Output: Excel file with only unique, non-duplicate records

### `validation/address_similarity.py`
Calculates fuzzy similarity scores for address pairs.

- Uses `thefuzz` library's `token_sort_ratio` method
- Scores range from 0 (no match) to 100 (identical)
- Resilient to word order differences and minor typos
- Output: Excel file with similarity scores for sorting/filtering

## Sample Data

The `samples/` directory contains small test files:
- `sample_input.csv` — 5 example branch records with Google Maps links
- `sample_output.csv` — Expected output after coordinate extraction

## Dependencies

All dependencies are listed in the root `requirements.txt`. Key packages:
- `requests` — HTTP client for URL expansion and API calls
- `pandas` + `openpyxl` — Data manipulation and Excel I/O
- `thefuzz` + `python-Levenshtein` — Fuzzy string matching
- `python-dotenv` — Environment variable management
