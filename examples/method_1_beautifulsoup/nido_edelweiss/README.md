# Nido (Edelweiss Housing Finance)

**Method:** BeautifulSoup (Static HTML Parsing)
**Difficulty:** Beginner

## Overview

This scraper extracts branch data from Nido Home Finance (an Edelweiss Housing Finance
brand). The entire parser is approximately 60 lines, making it one of the most concise
scrapers in the collection. It parses branch address blocks from saved HTML and uses
regex-based state detection against a predefined list of all Indian states.

## What It Demonstrates

- State detection via regex word-boundary matching against a predefined state list
- Compact, minimal-dependency HTML parsing
- Clean single-pass extraction from address text blocks

### Key Technique

Detecting the state from unstructured address text:

```python
re.search(r'\b' + re.escape(state) + r'\b', text_block, re.IGNORECASE)
```

This iterates over a list of all Indian states and uses word-boundary anchors to find
which state appears in each address block. It handles multi-word states (e.g.,
"Madhya Pradesh") and is case-insensitive.

## Files

| File | Description |
|------|-------------|
| `parse_nido_html.py` | Main parser (~60 lines) that extracts branches from HTML |
| `nido_html_branches.csv` | Extracted branch data in CSV format |
| `nido_branches.xlsx` | Extracted branch data in Excel format |

## How to Run

### Prerequisites

```bash
pip install beautifulsoup4 pandas openpyxl
```

### Execution

```bash
python parse_nido_html.py
```

The script reads a locally saved HTML file from the Nido branch locator page,
parses each branch entry, detects the state from the address text, and writes
the structured output to CSV and XLSX.

## Output Fields

- Branch Name
- Address
- State (auto-detected from address text)

## Notes

- The state detection approach is reusable across many bank scrapers where the address
  text contains the state name but there is no dedicated state field.
- Save the HTML source from the Nido branch locator page before running.
