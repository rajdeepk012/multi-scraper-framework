# Scraping Method Gallery

Five distinct approaches used across 90+ Indian bank/NBFC branch scrapers, with live examples you can study and extend.

---

## Method 1: BeautifulSoup (HTTP + HTML Parsing)

**Speed**: Fast | **Complexity**: Low | **Fragility**: Low

Parse server-rendered HTML with `requests` + `BeautifulSoup`. No browser needed.

### Examples in this repo

| Bank | Key Technique |
|------|--------------|
| [CSL Finance](../examples/method_1_beautifulsoup/csl_finance/) | CSS-class targeting, coordinate extraction from `?q=` hrefs |
| [Nido/Edelweiss](../examples/method_1_beautifulsoup/nido_edelweiss/) | State detection via regex against predefined list |
| [Shubham Housing](../examples/method_1_beautifulsoup/shubham_housing/) | Extract JSON embedded in Next.js `<script>` tags |

### Signature Moves
- `requests.get()` with minimal headers
- `BeautifulSoup` to walk DOM elements by CSS class, tag, or attribute
- Regex for data cleanup: fixing malformed JSON, extracting coordinates from URLs
- Light and fast — no browser overhead

### When to Choose
- Pages are server-rendered with predictable HTML
- No JavaScript required to load content
- Speed matters and infra cost should be low
- Data is embedded in HTML attributes or structured tags

---

## Method 2: Direct API Calls

**Speed**: Fast | **Complexity**: Medium | **Fragility**: Very Low

Replicate the XHR/fetch calls that the website's frontend makes. Get clean JSON directly.

### Examples in this repo

| Bank | Key Technique |
|------|--------------|
| [APAC Finance](../examples/method_2_direct_api/apac_finance/) | Two-tier API: states endpoint → branches endpoint → details |
| [ICICI HFC](../examples/method_2_direct_api/icici_hfc/) | API with predefined city/state parameter lists |
| [IndusInd Bank](../examples/method_2_direct_api/indusind_bank/) | Single JSON dump — simplest possible scraper (~30 lines) |

### Signature Moves
- Open browser DevTools → Network tab → find XHR requests
- Replicate exact headers, cookies, and parameters in Python
- Responses are clean JSON — normalize directly to CSV
- Chain multiple API calls: discover IDs from one endpoint, fetch details from another

### When to Choose
- A JSON/XML API exists behind the UI (check Network tab for XHR calls)
- Dynamic tables loaded from `admin-ajax.php`, REST endpoints, or GraphQL
- HTML parsing would be brittle (frequently changing markup)
- You need the most stable, maintainable scraper

### Cookie Management
Some APIs require session cookies (XSRF tokens, session IDs). These expire and must be refreshed:
1. Visit the site in a browser
2. Open DevTools → Network → copy the Cookie header from any XHR request
3. Paste into your script's headers dict

---

## Method 3: Playwright (Headless Browser)

**Speed**: Medium | **Complexity**: Medium | **Fragility**: Medium

Use a real browser engine to handle JavaScript rendering, pagination, and dynamic content.

### Examples in this repo

| Bank | Key Technique |
|------|--------------|
| [Shivalik Bank](../examples/method_3_playwright/shivalik_bank/) | Both Playwright AND requests versions for comparison |
| [Protium](../examples/method_3_playwright/protium/) | Browser scraper + separate CSV post-processing step |

### Signature Moves
- `playwright.chromium.launch()` with optional stealth mode
- `page.wait_for_selector()` for dynamic content
- DOM parsing with BeautifulSoup on the rendered HTML
- Async batches with `asyncio` for concurrent page scraping

### When to Choose
- Content is rendered client-side (React/Vue/Angular SPA)
- Requires button clicks, dropdown selections, or pagination
- CSRF tokens only appear after JavaScript execution
- Anti-bot detection blocks plain HTTP requests

### Setup
```bash
pip install playwright
python -m playwright install chromium
```

---

## Method 4: Selenium (Browser Automation)

**Speed**: Slow | **Complexity**: High | **Fragility**: Medium-High

Full browser automation for complex interaction patterns — nested dropdowns, CDP network interception, multi-step forms.

### Examples in this repo

| Bank | Key Technique |
|------|--------------|
| [ART Housing](../examples/method_4_selenium/art_housing/) | Chrome DevTools Protocol (CDP) to capture AJAX responses |
| [Saraswat Bank](../examples/method_4_selenium/saraswat_bank/) | Triple-nested dropdown with 4 fallback extraction methods |
| [TVS Credit](../examples/method_4_selenium/tvs_credit/) | Iterative evolution: Selenium v1 → v2 → v3 → API version |

### Signature Moves
- `webdriver.Chrome()` with headless options and custom user agent
- CDP performance logging: `driver.execute_cdp_cmd('Network.enable', {})` to intercept AJAX
- `Select()` for dropdown navigation with explicit waits
- Multiple fallback strategies when primary extraction fails

### When to Choose
- Complex multi-step interactions (cascading dropdowns, form submissions)
- Need to intercept network traffic (CDP performance logs)
- Playwright doesn't support a specific browser feature you need
- Legacy sites with specific browser compatibility requirements

### The TVS Credit Story
The TVS Credit example is especially educational — it shows real-world scraper evolution:
1. **v1**: Basic Selenium, clicks through every branch
2. **v2**: Optimized waits and error handling
3. **v3**: Added coordinate extraction
4. **API version**: Discovered the underlying API and eliminated the browser entirely

This progression is how most professional scrapers evolve.

---

## Method 5: Hybrid Approaches

**Speed**: Varies | **Complexity**: High | **Fragility**: Varies

Combine multiple techniques: AJAX + session management, custom JSON parsing, CSRF token extraction.

### Examples in this repo

| Bank | Key Technique |
|------|--------------|
| [Aavas](../examples/method_5_hybrid/aavas/) | AJAX + session cookies + CSRF tokens + pincode extraction |
| [SK Finance](../examples/method_5_hybrid/sk_finance/) | Bracket-depth parsing of JSON from Next.js server-rendered HTML |

### Signature Moves
- Manual session management: extract PHPSESSID + CSRF token from browser
- Multi-stage data collection: scrape states → branches → details → pincodes
- Custom JSON parsing when standard `json.loads()` fails on embedded data
- Bracket-depth counting to find JSON boundaries in messy HTML

### When to Choose
- No single method works end-to-end
- Session/auth tokens are required but can't be automated
- Data is embedded in non-standard formats (Next.js hydration payloads)
- Multiple post-processing steps needed (geocoding, pincode extraction)

---

## Quick Decision Guide

```
Is there a JSON API in the Network tab?
├── YES → Method 2 (Direct API)
└── NO
    ├── Is the page server-rendered HTML?
    │   ├── YES → Method 1 (BeautifulSoup)
    │   └── NO (SPA / JS-rendered)
    │       ├── Simple JS rendering? → Method 3 (Playwright)
    │       └── Complex interactions? → Method 4 (Selenium)
    └── Need session tokens + custom parsing? → Method 5 (Hybrid)
```

## Battle-Tested Patterns

- **Pagination until empty**: Keep requesting `?page=N` until the response contains no results
- **Async batches with capped concurrency**: Process N pages at a time, not all at once
- **Coordinate enrichment**: Expand Google Maps short URLs with `coordinate_extractor.py`
- **Data quality**: Run `find_duplicates.py` after merging sources; use `address_similarity.py` to flag anomalies
