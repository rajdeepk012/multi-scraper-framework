# Aavas Financiers

**Method:** Hybrid (AJAX + Session Cookies)
**Difficulty:** Advanced

## Overview

This scraper extracts branch data from Aavas Financiers, whose website requires valid
PHP session cookies and CSRF tokens for its AJAX endpoints. The approach combines browser
session capture with direct HTTP requests: you visit the site in a browser to obtain
session credentials, then use those credentials in Python requests to call the AJAX
endpoints directly.

## What It Demonstrates

- Working with AJAX endpoints that require session cookies and CSRF tokens
- Two-tier API pattern: states endpoint -> branch details endpoint
- Session credential capture workflow (browser -> Python)
- Pincode extraction as a post-processing enrichment step

### Key Workflow

1. Visit the Aavas branch locator in your browser
2. Copy `PHPSESSID` and `csrfToken` from browser DevTools
3. Use `aavas_state.py` to explore the states API
4. Use `aavas_branch.py` to explore the branch detail API
5. Run `extract_aavas_data.py` with fresh cookies to scrape all branches
6. Run `extract_pincodes.py` to add pincodes from addresses

## Files

| File | Description |
|------|-------------|
| `extract_aavas_data.py` | Main scraper using session cookies for AJAX calls |
| `aavas_state.py` | API exploration script for the states endpoint |
| `aavas_branch.py` | API exploration script for branch details |
| `extract_pincodes.py` | Post-processor that extracts pincodes from addresses |
| `aavas_branches_completed.csv` | Final branch data in CSV format |
| `aavas_branches_completed.xlsx` | Final branch data in Excel format |

## How to Run

### Prerequisites

```bash
pip install requests pandas openpyxl
```

### Step 1: Obtain Session Cookies

1. Open the Aavas branch locator page in your browser
2. Open DevTools (F12) -> Application tab -> Cookies
3. Copy the values for `PHPSESSID` and `csrfToken`
4. Update the cookie headers in the scripts

### Step 2: Scrape Branch Data

```bash
python extract_aavas_data.py
```

### Step 3: Extract Pincodes

```bash
python extract_pincodes.py
```

## Important Notes

- **All scripts with Cookie headers need fresh `PHPSESSID` and `csrfToken` values.**
  These expire after the PHP session times out (typically 15-30 minutes of inactivity).
- The CSRF token must match the session; you cannot mix tokens from different sessions.
- This session-based AJAX pattern is common across many Indian NBFC and HFC websites
  built on PHP frameworks like Laravel or CodeIgniter.
