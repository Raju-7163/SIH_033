import urllib.request
import json

crops = ['Wheat', 'Rice', 'Maize', 'Sugarcane', 'Cotton', 'Soybean', 'Mustard', 'Groundnut', 'Onion', 'Potato', 'Tomato', 'Mango', 'Banana', 'Coconut', 'Jute']

results = {}

for c in crops:
    try:
        url = f'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={c}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            if 'original' in pages[page_id]:
                img_url = pages[page_id]['original']['source']
                results[c] = img_url
            else:
                results[c] = None
    except Exception as e:
        print(f"Error for {c}: {e}")

with open('new_urls.json', 'w') as f:
    json.dump(results, f, indent=4)
