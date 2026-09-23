import os
filepath = 'templates/base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

script_to_inject = '''
<script>
    window.cropImages = {};
    fetch('/static/data/crop_images.json')
        .then(res => res.json())
        .then(data => {
            window.cropImages = data;
        })
        .catch(err => console.error('Failed to load crop images map', err));

    window.handleImageFallback = function(img, cropName) {
        if (img.dataset.fallbackTried) return; // prevent infinite loop
        img.dataset.fallbackTried = "true";
        if (window.cropImages && window.cropImages[cropName]) {
            img.src = window.cropImages[cropName];
        } else {
            img.src = '/static/images/no-image.svg';
        }
    };
</script>
'''

if 'window.handleImageFallback' not in content:
    content = content.replace('<body>', '<body>' + script_to_inject)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
