# Shubham Housing

**Method:** BeautifulSoup (Static HTML Parsing)
**Difficulty:** Intermediate

## Overview

This scraper extracts branch data from Shubham Housing Finance's website, which is built
on Next.js. The branch data is not rendered in plain HTML elements but is instead embedded
as JSON inside `<script>` tags used by Next.js for server-side hydration. The script
locates these script tags, unescapes the JSON payload, and parses the branch records.

## What It Demonstrates

- Extracting structured JSON data embedded in Next.js `<script>` tags
- Using regex to locate `self.__next_f.push()` calls containing branch data
- Unescaping and parsing hydration payloads with `json.loads()`
- Handling Next.js-specific data serialization patterns

### Key Technique

Locating and extracting Next.js hydration data:

```python
# Find script tags containing Next.js push calls
# Extract the JSON substring from self.__next_f.push([...])
# Unescape and parse with json.loads()
```

The script searches for `self.__next_f.push()` patterns in script tags, extracts the
embedded JSON string, and deserializes it to access the branch data array containing
state, branch name, address, and coordinates.

## Files

| File | Description |
|------|-------------|
| `extract_shubham_data.py` | Main scraper that extracts JSON from Next.js script tags |
| `shubham_branches.csv` | Extracted branch data in CSV format |
| `shubham_branches.xlsx` | Extracted branch data in Excel format |

## How to Run

### Prerequisites

```bash
pip install beautifulsoup4 pandas openpyxl
```

### Execution

```bash
python extract_shubham_data.py
```

The script reads the saved HTML page, finds the Next.js hydration script tags,
extracts and parses the embedded JSON, and writes branch records to CSV and XLSX.

## Output Fields

- Branch Name
- Address
- State
- Latitude / Longitude

## Notes

- Next.js embeds data differently across versions. This approach targets the
  `self.__next_f.push()` pattern used by the version running on Shubham's site.
- This technique is applicable to many modern Next.js-based financial websites.
- Save the full HTML source (including all script tags) before running.
