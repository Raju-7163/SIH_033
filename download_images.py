import os
import urllib.request

os.makedirs('static/images', exist_ok=True)

images = {
    'hero-farmer.jpg': 'https://images.unsplash.com/photo-1595841696677-6489ff3f8cd1?w=800&q=80',
    'market-bg.jpg': 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?w=500&q=80',
    'default-crop.jpg': 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=400',
    'fallback-crop.jpg': 'https://images.unsplash.com/photo-1599940824399-b87987ceb72a?w=400&q=80'
}

for filename, url in images.items():
    filepath = os.path.join('static/images', filename)
    print(f'Downloading {url} to {filepath}...')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f'Successfully downloaded {filename}')
    except Exception as e:
        print(f'Failed to download {filename}: {e}')
