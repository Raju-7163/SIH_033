import urllib.request
import json
url = 'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles=Mustard_plant'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    pages = data['query']['pages']
    page_id = list(pages.keys())[0]
    print(pages[page_id]['original']['source'])
