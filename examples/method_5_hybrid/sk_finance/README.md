# SK Finance

**Method:** Hybrid (Next.js JSON Extraction)
**Difficulty:** Advanced

## Overview

This scraper extracts branch data from SK Finance's website, which uses Next.js to
embed branch data as a deeply nested JSON payload in the server-rendered HTML. Standard
regex-based JSON extraction fails due to the nesting depth and complexity. The script
uses a bracket-depth counting algorithm to correctly identify JSON boundaries within
the HTML source.

## What It Demonstrates

- Bracket-depth parsing to extract JSON from complex HTML payloads
- Handling deeply nested Next.js server-rendered data structures
- Why simple regex fails for complex JSON extraction and what to use instead
- Alternative extraction approaches for the same data source

### Key Technique

Bracket-depth counting to find JSON boundaries:

```python
# Start at the opening '{' or '['
# Increment depth on '{' and '[', decrement on '}' and ']'
# The JSON block ends when depth returns to 0
depth = 0
for i, char in enumerate(text[start:]):
    if char in '{[':
        depth += 1
    elif char in '}]':
        depth -= 1
    if depth == 0:
        json_str = text[start:start + i + 1]
        break
```

This approach reliably extracts valid JSON regardless of nesting depth, handling
cases where regex-based methods would either miss data or capture malformed substrings.

## Files

| File | Description |
|------|-------------|
| `extract_sk_branches.py` | Main scraper using bracket-depth JSON parsing |
| `extract_sk_finance_data.py` | Alternative extraction approach |
| `sk_branches.csv` | Extracted branch data in CSV format |
| `sk_finance_branch.xlsx` | Extracted branch data in Excel format |

## How to Run

### Prerequisites

```bash
pip install beautifulsoup4 requests pandas openpyxl
```

### Execution

```bash
python extract_sk_branches.py
```

The script fetches the SK Finance branch page, locates the Next.js data payload in
the HTML, uses bracket-depth counting to extract the JSON, parses it, and writes the
structured branch data to CSV and XLSX.

## Notes

- The raw JSON dump from the page is approximately 2.2MB. It and any intermediate
  text files are excluded from the repository; only processed output is included.
- The bracket-depth technique is a general-purpose tool for extracting JSON from any
  HTML source where the payload is too complex for regex.
- This is one of the more advanced parsing techniques in the collection and is worth
  studying if you encounter Next.js sites with embedded data.
