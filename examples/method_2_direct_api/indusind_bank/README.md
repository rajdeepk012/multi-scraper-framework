# IndusInd Bank

**Method:** Direct API
**Difficulty:** Beginner

## Overview

This is the simplest scraper in the entire collection. IndusInd Bank's branch locator
loads all branch data in a single JSON API response. The entire scraper is under 30 lines
of Python -- it fetches the JSON endpoint, parses the response, and writes the structured
data to CSV and Excel files.

## What It Demonstrates

- The simplest possible scraping approach: single API call, direct JSON parsing
- Minimal code needed when a bank exposes all data in one endpoint
- Clean JSON-to-DataFrame conversion with pandas

### Key Technique

```python
response = requests.get(api_url)
data = response.json()
df = pd.DataFrame(data)
```

When a branch locator returns all data in a single JSON response, no pagination,
iteration, or authentication is needed.

## Files

| File | Description |
|------|-------------|
| `extract_indusind_data.py` | Complete scraper in under 30 lines |
| `indusind_branches.csv` | Extracted branch data in CSV format |
| `indusind_branch.xlsx` | Extracted branch data in Excel format |

## How to Run

### Prerequisites

```bash
pip install requests pandas openpyxl
```

### Execution

```bash
python extract_indusind_data.py
```

The script fetches the JSON API, parses all branch records, and writes the output
files. Execution takes only a few seconds.

## Output Fields

- Branch Name
- Address
- City / State
- Latitude / Longitude
- Contact details

## Notes

- The raw JSON dump from the API is approximately 2.1MB and is excluded from the
  repository. Only the processed CSV and XLSX outputs are included.
- This is the ideal starting point if you are new to web scraping -- it demonstrates
  the best-case scenario where the data is freely accessible via a clean API.
- If the API endpoint changes or starts requiring authentication, you may need to
  inspect the branch locator page with browser DevTools to find the updated URL.
