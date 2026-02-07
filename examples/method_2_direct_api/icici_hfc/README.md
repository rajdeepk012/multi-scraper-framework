# ICICI Home Finance

**Method:** Direct API
**Difficulty:** Intermediate

## Overview

This scraper extracts branch data from ICICI Home Finance Company using their branch
locator API endpoint. The API accepts city and state parameters from predefined lists.
The scraper iterates through all city/state combinations to collect complete branch data.
A separate script enriches the results with geographic coordinates using the Google
Geocoding API.

## What It Demonstrates

- Calling a branch locator API with predefined city/state parameter lists
- Iterating through parameter combinations for complete data extraction
- Coordinate enrichment via the Google Geocoding API as a post-processing step
- Handling API responses with consistent JSON structure

### Key Workflow

1. Run `icici_hfc_scraper.py` to scrape all branches via the API
2. Run `add_icici_hfc_coords.py` to geocode addresses and add lat/lon

## Files

| File | Description |
|------|-------------|
| `icici_hfc_scraper.py` | Main scraper that iterates city/state combinations |
| `icici_hfc.py` | Alternative scraping approach |
| `add_icici_hfc_coords.py` | Geocoding script that adds coordinates via Google API |
| `icici_hfc_branches.csv` | Raw branch data without coordinates |
| `icici_hfc_branches_with_coords.csv` | Branch data enriched with coordinates |
| `icici_hfc_branches_with_coord.xlsx` | Final enriched data in Excel format |

## How to Run

### Prerequisites

```bash
pip install requests pandas openpyxl python-dotenv
```

### Execution

```bash
# Step 1: Scrape branch data
python icici_hfc_scraper.py

# Step 2: Add coordinates (requires Google API key)
python add_icici_hfc_coords.py
```

## Important Notes

- **Google API key required:** The geocoding script `add_icici_hfc_coords.py` requires
  a `GOOGLE_GEOCODE_API_KEY` environment variable. Set it in a `.env` file in the
  project directory:
  ```
  GOOGLE_GEOCODE_API_KEY=your_api_key_here
  ```
- The Google Geocoding API has usage limits and costs. Review the
  [pricing page](https://developers.google.com/maps/documentation/geocoding/usage-and-billing)
  before running on large datasets.
- The main scraper does not require any API key or authentication.
