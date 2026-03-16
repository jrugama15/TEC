import urllib.request
import ssl
import re
import json
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
BASE = "https://www.tecnacional.edu.ni"

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        return response.read().decode('utf-8')

# =========================================================
# STEP 1: Get list of all centers from the centros page
# =========================================================
print("=== FETCHING CENTERS LIST ===")
try:
    html = fetch(BASE + "/centros/")
    print(f"Centers page: {len(html)} bytes")
except:
    try:
        html = fetch(BASE + "/centro/")
        print(f"Centro page: {len(html)} bytes")
    except Exception as e:
        print(f"Error: {e}")
        html = ""

# Find center links
center_links = []
for m in re.finditer(r'<a[^>]+href=["\'](/centro/[^"\']+)["\']', html):
    link = m.group(1)
    if link not in [c['url'] for c in center_links]:
        center_links.append({'url': link})

print(f"Found {len(center_links)} unique center links")

# If we didn't find centers on /centros/, let's try another approach
if len(center_links) == 0:
    # Try the main page or search for center links
    main_html = fetch(BASE + "/")
    for m in re.finditer(r'<a[^>]+href=["\'](/centro/[^"\']+)["\']', main_html):
        link = m.group(1)
        if link not in [c['url'] for c in center_links]:
            center_links.append({'url': link})
    print(f"Found {len(center_links)} center links from main page")

# Print first 10 to verify
for c in center_links[:10]:
    print(f"  {c['url']}")

print(f"\nTotal centers to scrape: {len(center_links)}")
