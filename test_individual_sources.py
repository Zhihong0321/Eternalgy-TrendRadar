import requests
import time

# Test each source individually
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

print(f"Testing {len(all_sources)} sources individually...")
print()

working = []
empty = []
errors = []

for source_id in all_sources:
    try:
        response = requests.get(
            f"https://eternalgy-newsnow-production.up.railway.app/api/s?id={source_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if 'error' in data or data.get('statusCode') == 500:
                errors.append({
                    'id': source_id,
                    'message': data.get('message', 'Unknown error')
                })
                print(f"✗ {source_id}: ERROR - {data.get('message', 'Unknown')[:60]}")
            else:
                items_count = len(data.get('items', []))
                if items_count > 0:
                    working.append({'id': source_id, 'count': items_count})
                    print(f"✓ {source_id}: {items_count} items")
                else:
                    empty.append(source_id)
                    print(f"○ {source_id}: 0 items (empty)")
        else:
            errors.append({
                'id': source_id,
                'message': f"HTTP {response.status_code}"
            })
            print(f"✗ {source_id}: HTTP {response.status_code}")
            
    except Exception as e:
        errors.append({
            'id': source_id,
            'message': str(e)
        })
        print(f"✗ {source_id}: {str(e)[:60]}")
    
    time.sleep(0.5)  # Be nice to the server

print()
print("=" * 60)
print(f"Summary:")
print(f"  Working with items: {len(working)}")
print(f"  Empty (no items): {len(empty)}")
print(f"  Errors: {len(errors)}")
print()

if working:
    print("Working sources:")
    for item in working:
        print(f"  - {item['id']}: {item['count']} items")
