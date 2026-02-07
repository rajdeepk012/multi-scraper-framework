# Protium Finance

**Method:** Playwright (Browser Automation)
**Difficulty:** Intermediate

## Overview

This scraper extracts branch data from Protium Finance using Playwright for browser-based
scraping, followed by a separate CSV post-processing step to clean and fix the raw output.
The two-phase workflow (scrape then clean) is a common pattern when the raw scraped data
needs normalization or error correction before it is ready for use.

## What It Demonstrates

- Browser-based scraping with Playwright for JavaScript-rendered content
- Two-phase workflow: raw data extraction followed by CSV post-processing
- Data cleaning and fixing as a separate, repeatable step
- Multiple scraper implementations for the same target

### Key Workflow

1. Run the browser scraper to collect raw branch data with coordinates
2. Run the CSV fixer to clean, deduplicate, and normalize the output

## Files

| File | Description |
|------|-------------|
| `protium_browser_scraper.py` | Main Playwright-based scraper |
| `protium_scraper.py` | Alternative scraping approach |
| `fix_protium_csv.py` | Post-processing script to clean and fix the raw CSV |
| `protium_branches_with_coords.csv` | Cleaned branch data with coordinates |
| `protium_branches_with_coord.xlsx` | Final cleaned data in Excel format |

## How to Run

### Prerequisites

```bash
pip install playwright pandas openpyxl
playwright install chromium
```

### Execution

```bash
# Step 1: Scrape branch data using browser automation
python protium_browser_scraper.py

# Step 2: Clean and fix the output CSV
python fix_protium_csv.py
```

## Output Fields

- Branch Name
- Address
- City / State
- Latitude / Longitude
- Pincode

## Notes

- The Playwright scraper launches a headless Chromium browser to render the page and
  extract branch data that is loaded dynamically via JavaScript.
- The `fix_protium_csv.py` script handles common issues such as malformed rows, encoding
  problems, and inconsistent formatting in the raw scraped data.
- If the browser scraper fails, ensure Chromium is installed via `playwright install`.
