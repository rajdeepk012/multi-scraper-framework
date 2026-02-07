# Data Pipeline Overview

End-to-end walkthrough of how raw bank branch data goes from a website to a clean, geocoded, deduplicated dataset.

---

## Pipeline Stages

```
┌─────────────┐    ┌──────────────┐    ┌────────────┐    ┌──────────────┐
│  1. SCRAPE   │───>│  2. GEOCODE   │───>│ 3. VALIDATE │───>│  4. EXPORT   │
│  Raw HTML/   │    │  Add coords   │    │  Dedup +    │    │  Final CSV/  │
│  API → CSV   │    │  + pincodes   │    │  compare    │    │  XLSX        │
└─────────────┘    └──────────────┘    └────────────┘    └──────────────┘
```

---

## Stage 1: Scraping

**Goal**: Extract branch data (name, address, city, state) from a financial institution's website.

### Process
1. **Reconnaissance**: Visit the branch locator page. Open browser DevTools → Network tab.
2. **Method Selection**: Based on what you see (see [DECISION_FLOWCHART.md](DECISION_FLOWCHART.md)):
   - JSON API calls? → Direct API method
   - Server-rendered HTML? → BeautifulSoup
   - JavaScript-rendered? → Playwright or Selenium
3. **Script Development**: Write an extraction script (see `examples/` for 13 templates).
4. **Output**: CSV file with columns like `State, City, Branch, Address`.

### Common Patterns
- **State iteration**: Loop through Indian states, fetch branches per state
- **Pagination**: Keep requesting `?page=N` until empty response
- **Two-tier APIs**: First call returns IDs, second call returns details
- **Embedded data**: Parse JSON from `<script>` tags or HTML attributes

### Output Format
All scrapers produce CSV files with at minimum:
```
State, City/Branch, Address
```
Many also include: `Latitude, Longitude, Phone, Email, Branch Code`

---

## Stage 2: Geocoding

**Goal**: Enrich branch data with geographic coordinates (latitude/longitude) and standardized pincodes.

### Two Sub-approaches

#### A. Google Maps URL Expansion (`coordinate_extractor.py`)
Used when the branch locator page contains Google Maps links (shortened or embedded).

```
Shortened URL → HEAD request → Follow redirects → Extract @lat,lng from final URL
```

- Handles 4 URL formats: `@lat,lng`, `?ll=`, `?lat=&lng=`, `/place/@lat,lng`
- 8 concurrent workers for speed
- ~98% success rate on shortened URLs
- Incremental saves every 25 records (crash-safe)

#### B. Address Geocoding (`address_geocoder.py`)
Used when no Maps links are available — sends addresses to Google Geocoding API.

```
Address string → Google Geocoding API → Formatted address + pincode + lat/lng
```

- Requires Google Maps API key (see `.env.example`)
- Returns: formatted address, pincode, city, state, latitude, longitude
- Rate-limited to 50ms between requests

### When to Use Which
| Scenario | Tool |
|----------|------|
| Branch page has Google Maps links | `coordinate_extractor.py` |
| Only text addresses available | `address_geocoder.py` |
| Maps links are embedded (`/maps/embed`) | Parse `!2d` (lng) and `!3d` (lat) from URL params |

---

## Stage 3: Validation

**Goal**: Ensure data quality by comparing against existing records and removing duplicates.

### Step 3a: Pincode Comparison (`compare_by_pincode.py`)
Matches branches between existing (e.g., Salesforce) data and newly scraped data using 6-digit Indian pincodes.

```python
# Extract pincode from address
pincode = re.search(r'\b(\d{6})\b', address)
# Inner merge on pincode → side-by-side comparison
```

Output: Excel file showing `Pincode | Existing Address | Scraped Address`

### Step 3b: Duplicate Detection (`find_duplicates.py`)
Identifies records that already exist in your database.

```python
# Normalize: lowercase → remove punctuation → extract pincode
# Create match key: normalized_address + "_" + pincode
# Set-based O(1) lookup against existing records
```

Output: Excel file with only unique, new records to add.

### Step 3c: Fuzzy Address Matching (`address_similarity.py`)
Calculates similarity scores for address pairs that matched by pincode.

```python
# thefuzz token_sort_ratio: ignores word order, handles typos
score = fuzz.token_sort_ratio("123 Main St, Delhi", "Main Street 123, New Delhi")
# Returns: 85 (high similarity)
```

Output: Excel file with 0-100 similarity scores for manual review.

---

## Stage 4: Export

**Goal**: Produce the final clean dataset.

### Final Output Columns
```
State, City, Branch Name, Address, Pincode, Latitude, Longitude
```

### Formats
- **CSV**: For programmatic use, database import, further processing
- **XLSX**: For manual review, sharing with non-technical stakeholders

### Quality Checks
Before declaring the dataset complete:
1. Row count matches expected number of branches (cross-reference with the website)
2. No duplicate pincodes within the same branch name
3. Coordinates fall within India's geographic bounds (lat: 8-37, lng: 68-97)
4. Pincode format: exactly 6 digits, no leading zeros stripped

---

## Real-World Scale

This pipeline has been used to process:
- **90+ financial institutions** (banks, NBFCs, housing finance companies)
- **15,000+ branch records** across all Indian states
- **5 distinct scraping methods** adapted to each institution's website
- Data feeds into Salesforce CRM for branch network management
