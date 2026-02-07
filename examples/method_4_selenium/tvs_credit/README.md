# TVS Credit Services

**Method:** Selenium (Evolutionary)
**Difficulty:** Advanced

## Overview

This folder documents the real-world evolution of a scraper through four iterations:
from a basic Selenium browser automation script to a pure API-based solution. Each
version represents a step in the reverse-engineering process, making this the most
educational example in the collection for understanding how to discover and migrate
to hidden APIs.

## What It Demonstrates

- Iterative scraper development: v1 -> v2 -> v3 -> pure API
- Reverse-engineering an API from browser automation observations
- The progression from slow browser scraping to fast direct API calls
- How to identify API endpoints by watching network traffic during Selenium runs

### Evolution Path

1. **v1** (`tvs_credit_scraper.py`): Basic Selenium, interacts with the UI directly
2. **v2** (`tvs_credit_scraper_v2.py`): Improved Selenium with better error handling
3. **v3** (`tvs_credit_scraper_v3.py`): Optimized Selenium with network observation
4. **API** (`tvs_credit_api_scraper.py`): Pure requests-based API scraper, no browser

## Files

| File | Description |
|------|-------------|
| `tvs_credit_scraper.py` | v1: Basic Selenium scraper |
| `tvs_credit_scraper_v2.py` | v2: Improved Selenium with better error handling |
| `tvs_credit_scraper_v3.py` | v3: Optimized Selenium, network traffic observation |
| `tvs_credit_api_scraper.py` | Final version: pure API scraper, no browser needed |
| `tvs_credit_branches.csv` | Branch data in CSV format |
| `tvs_credit_branches_with_coords.csv` | Branch data with geographic coordinates |
| `tvs_credit_branches_with_coord.xlsx` | Final data in Excel format |

## How to Run

### Prerequisites

```bash
# For Selenium versions (v1-v3)
pip install selenium pandas openpyxl webdriver-manager

# For API version (recommended)
pip install requests pandas openpyxl
```

### Execution (Recommended: API Version)

```bash
python tvs_credit_api_scraper.py
```

### Execution (Selenium Versions)

```bash
python tvs_credit_scraper.py      # v1
python tvs_credit_scraper_v2.py   # v2
python tvs_credit_scraper_v3.py   # v3
```

## Notes

- Start with the API version (`tvs_credit_api_scraper.py`) for production use. It is
  faster, more reliable, and does not require a browser.
- Read the Selenium versions in order (v1 -> v2 -> v3 -> API) to understand the
  reverse-engineering process.
- This pattern (browser automation -> API discovery) applies to many websites and is
  one of the most valuable skills in web scraping.
