import urllib.request
import ssl
import re
import json
import html as html_module
import time

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

# =========================================================
# Scrape education tecnica page to find sectors
# =========================================================
print("=== Fetching educacion-tecnica page ===")
page = fetch(BASE + "/educacion-tecnica/")
print(f"Page: {len(page)} bytes")

# Find sector links - they look like /educacion-tecnica/SECTOR_ID
sector_links = []
for m in re.finditer(r'<a[^>]+href=["\'](/educacion-tecnica/(\d+)/?)["\'][^>]*>(.*?)</a>', page, re.DOTALL):
    url = m.group(1)
    sector_id = m.group(2)
    name = clean(m.group(3))
    if name and len(name) > 2:
        exists = any(s['id'] == sector_id for s in sector_links)
        if not exists:
            sector_links.append({'id': sector_id, 'url': url, 'name': name})

print(f"Found {len(sector_links)} sectors:")
for s in sector_links:
    print(f"  [{s['id']}] {s['name']}")

# Now let's also look at the page structure for sector listings
# Check what's on the page
idx = page.find('col-md-4')
if idx != -1:
    print("\n=== Sector card structure ===")
    print(page[max(0,idx-100):idx+800])

# Also look for images associated with sectors
print("\n=== Looking for sector images ===")
for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\']', page):
    src = m.group(1)
    alt = m.group(2)
    if 'logo' not in src.lower() and 'social' not in src.lower():
        print(f"  {alt[:40]} -> {src[:80]}")
