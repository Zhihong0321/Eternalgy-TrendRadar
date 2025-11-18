import requests
import json

# Test single source
print("Testing single source API...")
response = requests.get("https://eternalgy-newsnow-production.up.railway.app/api/s?id=thestar")
print(f"Status: {response.status_code}")
data = response.json()
print(f"Response: {json.dumps(data, indent=2)}")
print()

# Test batch endpoint
print("Testing batch endpoint...")
sources = ["thestar", "malaymail", "nst", "bernama", "astroawani"]
response = requests.post(
    "https://eternalgy-newsnow-production.up.railway.app/api/s/entire",
    headers={"Content-Type": "application/json"},
    json={"sources": sources}
)
print(f"Status: {response.status_code}")
print(f"Raw response: {response.text[:500]}")
data = response.json()
print(f"Response type: {type(data)}")
print(f"Number of sources returned: {len(data) if isinstance(data, list) else 'N/A'}")
if isinstance(data, list):
    for source in data:
        print(f"  - {source['id']}: {len(source.get('items', []))} items, status: {source.get('status')}")
else:
    print(f"Unexpected response format: {data}")
print()

# Test with renewable energy sources
print("Testing renewable energy sources...")
renewable_sources = ["pvmagazine", "solarpowerworld", "cleantechnica"]
response = requests.post(
    "https://eternalgy-newsnow-production.up.railway.app/api/s/entire",
    headers={"Content-Type": "application/json"},
    json={"sources": renewable_sources}
)
print(f"Status: {response.status_code}")
data = response.json()
for source in data:
    if 'error' in source:
        print(f"  - {source.get('id', 'unknown')}: ERROR - {source.get('message', 'Unknown error')}")
    else:
        print(f"  - {source['id']}: {len(source.get('items', []))} items")
