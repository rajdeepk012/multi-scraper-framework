# Saraswat Cooperative Bank

**Method:** Selenium (Browser Automation)
**Difficulty:** Advanced

## Overview

This is one of the most complex scrapers in the collection. Saraswat Bank's branch
locator uses a triple-nested cascading dropdown system (Zone -> Region -> Branch).
The scraper must navigate every combination of these dropdowns and extract branch
details from each selection. It implements four different fallback extraction methods
to handle inconsistencies in how the page renders branch information.

## What It Demonstrates

- Navigating triple-nested cascading dropdown menus with Selenium
- Defensive coding with 4 fallback extraction strategies
- Handling dynamic page updates after dropdown selections
- Robust error recovery to avoid losing progress on partial failures

### Key Challenge

The cascading dropdowns mean the scraper must:

1. Select each Zone from the first dropdown
2. Wait for the Region dropdown to populate
3. Select each Region
4. Wait for the Branch dropdown to populate
5. Select each Branch and extract the displayed details

Each transition requires waiting for AJAX updates, and the page structure for
displaying branch details varies, necessitating multiple extraction strategies.

## Files

| File | Description |
|------|-------------|
| `sarswat_scraper.py` | Full scraper with triple-dropdown navigation and 4 fallback methods |
| `saraswat_branches.csv` | Extracted branch data in CSV format |
| `saraswat_branch.xlsx` | Extracted branch data in Excel format |

## How to Run

### Prerequisites

```bash
pip install selenium pandas openpyxl webdriver-manager
```

You also need Google Chrome installed on your system.

### Execution

```bash
python sarswat_scraper.py
```

The script launches Chrome, navigates through all Zone/Region/Branch combinations,
extracts branch details using whichever extraction method succeeds, and writes the
results to CSV and XLSX. Expect a longer runtime due to the number of dropdown
combinations and page wait times.

## Notes

- The four fallback extraction methods handle cases where branch details appear in
  different HTML structures (tables, divs, spans, or plain text).
- Runtime can be significant due to the large number of dropdown combinations and
  the wait time required between selections.
- If the script is interrupted, you may need to re-run from the beginning unless
  you add checkpointing logic.
