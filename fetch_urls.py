import urllib.request
import json
import re

def get_unsplash(query):
    try:
        req = urllib.request.Request(f'https://unsplash.com/napi/search/photos?query={query}&per_page=1', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            if data['results']:
                return data['results'][0]['urls']['small']
    except Exception as e:
        print("Error fetching", query, e)
    return None

crops = ['Wheat', 'Rice', 'Maize', 'Sugarcane', 'Cotton', 'Soybean', 'Mustard', 'Groundnut', 'Onion', 'Potato', 'Tomato', 'Mango', 'Banana', 'Coconut', 'Jute']

results = {}
for c in crops:
    url = get_unsplash(c + ' crop')
    if not url:
        url = get_unsplash(c)
    results[c] = url
    print(f'{c}: {url}')

with open('new_urls.json', 'w') as f:
    json.dump(results, f, indent=4)
