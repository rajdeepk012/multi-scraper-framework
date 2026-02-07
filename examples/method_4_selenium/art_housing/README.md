# ART Housing Finance

**Method:** Selenium (Chrome DevTools Protocol)
**Difficulty:** Advanced

## Overview

This scraper takes an unconventional approach: instead of parsing HTML elements, it uses
Selenium's Chrome DevTools Protocol (CDP) integration to intercept network responses.
The branch locator page makes AJAX requests to fetch branch data as JSON, and this script
captures those raw JSON responses directly from the network layer.

## What It Demonstrates

- Using Chrome DevTools Protocol (CDP) performance logging via Selenium
- Intercepting AJAX/XHR responses at the network level instead of parsing the DOM
- Extracting structured JSON from captured network traffic
- An alternative to HTML parsing when the data is loaded via background API calls

### Key Technique

Enabling CDP network capture and reading AJAX responses:

```python
# Enable network logging via CDP
driver.execute_cdp_cmd('Network.enable', {})

# Retrieve performance logs containing network events
logs = driver.get_log('performance')

# Filter for Network.responseReceived events and extract JSON bodies
```

This approach bypasses the rendered page entirely and reads the raw data as the
server sends it.

## Files

| File | Description |
|------|-------------|
| `art_scraper.py` | Selenium + CDP scraper that intercepts network responses |
| `art_branches.csv` | Extracted branch data in CSV format |
| `art_branch.xlsx` | Extracted branch data in Excel format |

## How to Run

### Prerequisites

```bash
pip install selenium pandas openpyxl webdriver-manager
```

You also need Google Chrome installed on your system.

### Execution

```bash
python art_scraper.py
```

The script launches Chrome with performance logging enabled, navigates to the branch
locator, captures the AJAX responses containing branch data, and writes the parsed
results to CSV and XLSX.

## Notes

- This technique is useful when a website loads data via AJAX but makes it difficult
  to extract from the rendered HTML (e.g., data inside canvas elements or complex
  JavaScript frameworks).
- CDP performance logging must be enabled before navigation for the logs to capture
  the relevant network events.
- Chrome must be installed; the script uses `webdriver-manager` to handle ChromeDriver.
