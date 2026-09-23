import urllib.request
import json

crops = ['Wheat', 'Rice', 'Maize', 'Sugarcane', 'Cotton', 'Soybean', 'Groundnut', 'Onion', 'Potato', 'Tomato', 'Mango', 'Banana', 'Coconut', 'Jute']
results = {}

for c in crops:
    url = f'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=thumbnail&pithumbsize=400&titles={c}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        pages = data['query']['pages']
        page_id = list(pages.keys())[0]
        if 'thumbnail' in pages[page_id]:
            results[c] = pages[page_id]['thumbnail']['source']

# Mustard
url = f'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=thumbnail&pithumbsize=400&titles=Mustard_plant'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    pages = data['query']['pages']
    page_id = list(pages.keys())[0]
    results['Mustard'] = pages[page_id]['thumbnail']['source']

with open('new_urls.json', 'w') as f:
    json.dump(results, f, indent=4)
