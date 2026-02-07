# CSL Finance

**Method:** BeautifulSoup (Static HTML Parsing)
**Difficulty:** Beginner

## Overview

This scraper extracts branch location data from CSL Finance's website. The site renders
branch information inside an accordion layout with specific CSS classes. The script parses
a saved HTML file, targets those classes to extract branch names and addresses, and pulls
latitude/longitude coordinates from Google Maps links embedded in button `href` attributes.

## What It Demonstrates

- Targeting specific CSS classes (`s__7YWojd`, `MJXUU`, `F3Ebu`) with BeautifulSoup
- Extracting geographic coordinates from Google Maps `href` links using regex
- Simple, single-file HTML-to-CSV pipeline

### Key Technique

Extracting coordinates from Google Maps links:

```python
re.search(r'q=([0-9\.\,]+)', href)
```

This regex captures the `?q=lat,lon` parameter that Google Maps uses in its link format,
giving you coordinates without needing a geocoding API.

## Files

| File | Description |
|------|-------------|
| `extract_csl_data.py` | Main scraper that parses the HTML and outputs structured data |
| `csl_finance_branches.csv` | Extracted branch data in CSV format |
| `csl_finance_branches.xlsx` | Extracted branch data in Excel format |

## How to Run

### Prerequisites

```bash
pip install beautifulsoup4 pandas openpyxl
```

### Execution

```bash
python extract_csl_data.py
```

The script reads a local HTML file, parses branch data from the accordion elements,
extracts coordinates from Google Maps links, and writes the results to CSV and XLSX.

## Output Fields

- Branch Name
- Address
- Latitude / Longitude (from Google Maps href)
- State

## Notes

- The HTML source file should be saved locally from the CSL Finance branch locator page
  before running the script.
- This is one of the simplest scrapers in the collection and serves as a good starting
  point for understanding the BeautifulSoup approach.
