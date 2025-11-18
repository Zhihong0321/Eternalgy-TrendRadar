import requests
import json

# All 26 sources from the documentation
all_sources = [
    # Renewable Energy (18)
    "pvmagazine", "solarpowerworld", "cleantechnica",
    "renewableenergyworld", "rechargenews", "utilitydive",
    "renewablesnow", "canarymedia", "solarindustrymag",
    "irena", "eia", "energystoragenews", "pvtech",
    "renewableenergyindustry", "solarbuildermag",
    "europeanenergyinnovation", "solarquarter", "renewableenergyfocus",
    
    # Malaysian News (8)
    "thestar", "malaysiakini", "freemalaysiatoday",
    "malaymail", "nst", "astroawani", "theedgemarkets", "bernama"
]

print(f"Testing batch endpoint with all {len(all_sources)} sources...")
print()

response = requests.post(
    "https://eternalgy-newsnow-production.up.railway.app/api/s/entire",
    headers={"Content-Type": "application/json"},
    json={"sources": all_sources},
    timeout=30
)

print(f"Status Code: {response.status_code}")
print(f"Response Length: {len(response.text)} bytes")
print()

try:
    data = response.json()
    
    if isinstance(data, list):
        print(f"✓ Received {len(data)} sources")
        print()
        
        # Summary
        successful = []
        with_items = []
        errors = []
        
        for source in data:
            source_id = source.get('id', 'unknown')
            
            if 'error' in source or source.get('statusCode') == 500:
                errors.append({
                    'id': source_id,
                    'message': source.get('message', 'Unknown error')
                })
            else:
                successful.append(source_id)
                items_count = len(source.get('items', []))
                if items_count > 0:
                    with_items.append({
                        'id': source_id,
                        'count': items_count,
                        'status': source.get('status'),
                        'updated': source.get('updatedTime')
                    })
        
        print(f"Summary:")
        print(f"  Successful: {len(successful)}/{len(all_sources)}")
        print(f"  With items: {len(with_items)}")
        print(f"  Errors: {len(errors)}")
        print()
        
        if with_items:
            print("Sources with news items:")
            for item in with_items:
                print(f"  ✓ {item['id']}: {item['count']} items (status: {item['status']})")
        
        if errors:
            print()
            print("Sources with errors:")
            for error in errors:
                print(f"  ✗ {error['id']}: {error['message']}")
        
        # Show sample item if available
        if with_items:
            print()
            print("Sample news item:")
            for source in data:
                if source.get('items') and len(source['items']) > 0:
                    item = source['items'][0]
                    print(f"  Source: {source['id']}")
                    print(f"  Title: {item.get('title', 'N/A')}")
                    print(f"  URL: {item.get('url', 'N/A')}")
                    print(f"  PubDate: {item.get('pubDate', 'N/A')}")
                    break
    else:
        print(f"Unexpected response format: {type(data)}")
        print(json.dumps(data, indent=2))
        
except Exception as e:
    print(f"Error parsing response: {e}")
    print(f"Raw response: {response.text[:1000]}")
