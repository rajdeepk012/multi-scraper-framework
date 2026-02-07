# Shivalik Small Finance Bank

**Method:** Playwright + Requests
**Difficulty:** Intermediate

## Overview

This folder contains two independent scraping approaches for the same target: a
Playwright browser automation version and a requests-based version using session cookies.
A third script parses a locally saved HTML file. Having multiple approaches makes this
a useful reference for comparing browser automation versus direct HTTP requests.

## What It Demonstrates

- Side-by-side comparison: Playwright (browser) vs. requests (HTTP) for the same site
- Session cookie management for authenticated endpoints
- Local HTML parsing as a fallback approach
- Trade-offs: Playwright handles sessions automatically but is slower; requests is
  faster but requires manual cookie management

## Files

| File | Description |
|------|-------------|
| `extract_shivalik_data_playwright.py` | Playwright version with automatic session handling |
| `extract_shivalik_data.py` | Requests version using manually provided session cookies |
| `parse_shivalik_local.py` | Local HTML parser for previously saved pages |
| `shivalik_branches_all.csv` | Extracted branch data in CSV format |
| `shivalik_branch.xlsx` | Extracted branch data in Excel format |

## How to Run

### Prerequisites

```bash
pip install playwright requests pandas openpyxl
playwright install chromium
```

### Option A: Playwright (Recommended)

```bash
python extract_shivalik_data_playwright.py
```

This version launches a headless browser, navigates the branch locator, and extracts
data automatically. No manual cookie setup required.

### Option B: Requests with Session Cookies

```bash
python extract_shivalik_data.py
```

### Option C: Local HTML Parsing

```bash
python parse_shivalik_local.py
```

## Important Notes

- **Session cookies for requests version:** `extract_shivalik_data.py` requires fresh
  `XSRF-TOKEN` and `sfsb_session` cookie values. Copy them from your browser's DevTools
  (Application tab > Cookies) after visiting the Shivalik branch locator page.
- The Playwright version is the recommended approach as it handles cookie/session
  management automatically.
- The local parser is useful if you have already saved the HTML pages and want to
  re-extract data without making network requests.
