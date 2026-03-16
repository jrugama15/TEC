import urllib.request
import ssl
import re
import json
import time
import html as html_module

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
BASE = "https://www.tecnacional.edu.ni"

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        return response.read().decode('utf-8')

def clean(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = html_module.unescape(text)
    return ' '.join(text.split()).strip()

# Load existing center data
with open('../data/centers.json', 'r', encoding='utf-8') as f:
    centers = json.load(f)

print(f"Loaded {len(centers)} centers, now fetching careers for each...")

for i, center in enumerate(centers):
    try:
        careers_url = BASE + center['url'] + "carreras/"
        page = fetch(careers_url)
        
        careers = []
        # Pattern: <div class="col-md-6 lista">...<img src="..."...><h4><a href="...">TITLE</a></h4><p>DESC</p>
        blocks = page.split('class="col-md-6 lista"')
        for b in blocks[1:]:
            # Image
            img_m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', b)
            img = ""
            if img_m:
                img = img_m.group(1)
                if img.startswith('/'): img = BASE + img
            
            # Title and URL
            a_m = re.search(r'<h4>\s*<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', b, re.DOTALL)
            if not a_m: continue
            career_url = a_m.group(1)
            career_name = clean(a_m.group(2))
            
            # Description
            desc_m = re.search(r'<p>(.*?)</p>', b, re.DOTALL)
            career_desc = clean(desc_m.group(1)) if desc_m else ""
            
            if career_url.startswith('/'):
                career_url = BASE + career_url
            
            careers.append({
                'name': career_name,
                'url': career_url,
                'image': img,
                'description': career_desc[:200]
            })
        
        center['careers'] = careers
        print(f"  [{i+1}/{len(centers)}] {center['title'][:45]} - {len(careers)} careers")
        time.sleep(0.2)
        
    except Exception as e:
        print(f"  [{i+1}/{len(centers)}] {center['title'][:45]} - ERROR: {e}")

with open('../data/centers.json', 'w', encoding='utf-8') as f:
    json.dump(centers, f, ensure_ascii=False, indent=2)

total = sum(len(c['careers']) for c in centers)
print(f"\nDone! Total careers across all centers: {total}")
