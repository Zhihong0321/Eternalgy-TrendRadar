# NewsNow API Test Results

**Test Date**: November 18, 2025  
**API Base URL**: `https://eternalgy-newsnow-production.up.railway.app/api`

## Summary

Out of 26 documented news sources, only **2 sources are currently functional**:

- ✓ **eia** (U.S. Energy Information Administration): 22 items
- ○ **thestar** (The Star Online): 0 items (working but empty)

**24 sources are returning HTTP 500 errors**, mostly with the message:
> "Cannot read properties of undefined (reading 'title')"

This suggests the RSS feeds may have changed format or are unavailable.

---

## API Endpoints Tested

### 1. Single Source Endpoint: `GET /api/s?id={sourceId}`

**Working Example**:
```bash
curl "https://eternalgy-newsnow-production.up.railway.app/api/s?id=eia"
```

**Response**:
```json
{
  "status": "cache",
  "id": "eia",
  "updatedTime": 1763388000000,
  "items": [
    {
      "id": "https://www.eia.gov/todayinenergy/detail.php?id=66645",
      "title": "U.S. rig counts remain low as production efficiencies improve",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=66645",
      "pubDate": 1763388000000
    }
    // ... 21 more items
  ]
}
```

### 2. Batch Endpoint: `POST /api/s/entire`

**Working Example**:
```bash
curl -X POST "https://eternalgy-newsnow-production.up.railway.app/api/s/entire" \
  -H "Content-Type: application/json" \
  -d '{"sources": ["eia", "thestar"]}'
```

**Response**: Returns array with only working sources (filters out errors)

---

## Detailed Source Status

### Renewable Energy Sources (18 total)

| Source ID | Status | Items | Error Message |
|-----------|--------|-------|---------------|
| pvmagazine | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| solarpowerworld | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| cleantechnica | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| renewableenergyworld | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| rechargenews | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| utilitydive | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| renewablesnow | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| canarymedia | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| solarindustrymag | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| irena | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| **eia** | ✅ **Working** | **22** | - |
| energystoragenews | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| pvtech | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| renewableenergyindustry | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| solarbuildermag | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| europeanenergyinnovation | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| solarquarter | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| renewableenergyfocus | ❌ Error | - | Cannot read properties of undefined (reading 'title') |

### Malaysian News Sources (8 total)

| Source ID | Status | Items | Error Message |
|-----------|--------|-------|---------------|
| **thestar** | ⚠️ **Empty** | **0** | - |
| malaysiakini | ❌ Error | - | [GET] "https://www.malaysiakini.com/feed/news.rss": 404 Not Found |
| freemalaysiatoday | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| malaymail | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| nst | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| astroawani | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| theedgemarkets | ❌ Error | - | Cannot read properties of undefined (reading 'title') |
| bernama | ❌ Error | - | Cannot read properties of undefined (reading 'title') |

---

## Sample Working Response (EIA)

```json
{
  "status": "cache",
  "id": "eia",
  "updatedTime": 1763388000000,
  "items": [
    {
      "id": "https://www.eia.gov/todayinenergy/detail.php?id=66645",
      "title": "U.S. rig counts remain low as production efficiencies improve",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=66645",
      "pubDate": 1763388000000
    }
  ]
}
```

---

## Python Integration Example

```python
import requests

def fetch_working_sources():
    """Fetch news from currently working sources"""
    working_sources = ["eia", "thestar"]
    
    response = requests.post(
        "https://eternalgy-newsnow-production.up.railway.app/api/s/entire",
        headers={"Content-Type": "application/json"},
        json={"sources": working_sources}
    )
    
    return response.json()

# Usage
sources = fetch_working_sources()
for source in sources:
    print(f"{source['id']}: {len(source['items'])} items")
```

---

## Recommendations

1. **Current State**: Only 2 out of 26 sources are functional
   - Most sources have RSS feed parsing errors
   - The API server may need maintenance to fix feed parsers

2. **For Your Project**: 
   - Focus on the working source (EIA) for now
   - Consider implementing fallback mechanisms
   - Monitor source status before making requests

3. **API Server Issues**:
   - RSS feed URLs may have changed
   - Feed formats may have been updated
   - Some feeds may be blocked or unavailable

4. **Next Steps**:
   - Contact the API maintainer about the errors
   - Consider alternative news sources
   - Implement error handling for unavailable sources

---

## Test Scripts

Three Python test scripts were created:

1. **test_api.py** - Basic API testing
2. **test_all_sources.py** - Batch endpoint testing
3. **test_individual_sources.py** - Individual source testing

Run any of these to verify current API status:
```bash
python test_individual_sources.py
```
