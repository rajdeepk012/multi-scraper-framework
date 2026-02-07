# APAC Financial Services

**Method:** Direct API
**Difficulty:** Intermediate

## Overview

This scraper extracts branch data from APAC Financial Services using a two-tier API
discovery approach. The workflow progresses from API exploration scripts to a production
scraper, then enriches the data with geographic coordinates extracted from embedded
Google Maps iframes. This folder shows the full development progression from discovery
to final output.

## What It Demonstrates

- Two-tier API discovery: states endpoint -> branch details endpoint
- Reverse-engineering API endpoints using browser DevTools
- Coordinate extraction from embedded Google Maps iframes
- Multi-script pipeline: explore -> scrape -> enrich with coordinates
- Working with session cookies for authenticated API requests

### Key Workflow

1. Use `apacfin_state.py` to discover the states API endpoint
2. Use `apacfin_branch.py` to explore the branch detail API
3. Run `extract_apacfin_data.py` to scrape all branches
4. Run `extract_apacfin_coords.py` / `process_apacfin_embed.py` to add coordinates

## Files

| File | Description |
|------|-------------|
| `apacfin_state.py` | API exploration script for the states endpoint |
| `apacfin_branch.py` | API exploration script for branch details |
| `extract_apacfin_data.py` | Main production scraper for all branches |
| `extract_apacfin_coords.py` | Coordinate extraction from map embeds |
| `process_apacfin_embed.py` | Processes embedded map URLs for coordinates |
| `apacfin_branches.csv` | Raw branch data without coordinates |
| `apacfin_branches_with_coords.csv` | Branch data enriched with coordinates |
| `apac_fin_branches_with_coords.xlsx` | Final enriched data in Excel format |

## How to Run

### Prerequisites

```bash
pip install requests pandas openpyxl
```

### Execution

```bash
# Step 1: Scrape branch data
python extract_apacfin_data.py

# Step 2: Enrich with coordinates
python extract_apacfin_coords.py
```

## Important Notes

- **Session cookies required:** The exploration scripts (`apacfin_state.py` and
  `apacfin_branch.py`) contain session cookie headers that expire. You must copy
  fresh cookie values from your browser's DevTools (Network tab) before running them.
- The main scraper `extract_apacfin_data.py` may also need updated session cookies
  depending on the site's authentication requirements.
- This folder is a good reference for understanding the API discovery workflow that
  applies to many Indian financial institution websites.
