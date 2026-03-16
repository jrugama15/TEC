import urllib.request
import ssl
import re
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE = "https://www.tecnacional.edu.ni"

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as response:
        return response.read().decode('utf-8')

# Step 1: Get gallery listing
html = fetch(BASE + "/galerias/")
print(f"Fetched listing: {len(html)} bytes")

# Parse gallery entries
galleries = []
blocks = html.split('<div class="list3-galeria')
for b in blocks[1:]:
    # Cover image
    img_m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', b)
    cover = img_m.group(1) if img_m else ""
    if cover.startswith('/'): cover = BASE + cover
    
    # Link and title
    link_m = re.search(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', b, re.DOTALL)
    if not link_m: continue
    link = link_m.group(1)
    if link.startswith('/'): link = BASE + link
    
    # Title from h1
    title_m = re.search(r'<h1>\s*<a[^>]*>(.*?)</a>', b, re.DOTALL)
    title = title_m.group(1).strip() if title_m else "Galería"
    # Clean HTML entities
    title = title.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    
    galleries.append({
        'title': title,
        'cover': cover,
        'link': link,
        'images': []
    })
    
    if len(galleries) == 5:
        break

print(f"Found {len(galleries)} galleries")
for g in galleries:
    print(f"  - {g['title']}")
    print(f"    Cover: {g['cover']}")
    print(f"    Link: {g['link']}")

# Step 2: Fetch each gallery detail to get individual images
for g in galleries:
    try:
        detail_html = fetch(g['link'])
        # Find gallery images - look for img tags in gallery content
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+(?:\.jpg|\.png|\.jpeg)[^"\']*)["\']', detail_html, re.IGNORECASE)
        # Filter for media images only
        media_imgs = []
        for img in imgs:
            if '/media/' in img and 'logo' not in img.lower() and 'social' not in img.lower() and 'Logo' not in img and 'not-found' not in img:
                full = img if img.startswith('http') else BASE + img
                if full not in media_imgs:
                    media_imgs.append(full)
        g['images'] = media_imgs[:8]  # max 8 images per gallery
        print(f"  Gallery '{g['title'][:40]}': {len(g['images'])} images")
    except Exception as e:
        print(f"  Error fetching {g['link']}: {e}")

# Save to JSON
with open('../data/galleries.json', 'w', encoding='utf-8') as f:
    json.dump(galleries, f, ensure_ascii=False, indent=2)

print("\nSaved to galleries.json")
