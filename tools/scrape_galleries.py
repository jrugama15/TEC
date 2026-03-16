import urllib.request
import ssl
import re
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Step 1: Fetch the galleries listing page
url = "https://www.tecnacional.edu.ni/galerias/"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read().decode('utf-8')
    print(f"Fetched galleries page: {len(html)} bytes")
except Exception as e:
    print("Error fetching galleries:", e)
    html = ""

# Let's inspect the structure
# Find gallery blocks
idx = html.find('galeria')
if idx == -1:
    idx = html.find('gallery')
if idx == -1:
    idx = html.find('col-md')

print(f"\nFirst relevant index: {idx}")

# Let's dump a chunk around a gallery entry to understand the HTML structure
# Search for image tags that look like gallery covers
img_matches = list(re.finditer(r'<img[^>]+src=["\']([^"\']*(?:900x450|280x170|galeria)[^"\']*)["\']', html, re.IGNORECASE))
print(f"\nFound {len(img_matches)} gallery-style images")
for m in img_matches[:10]:
    print("  IMG:", m.group(1))

# Let's also search for any div structure with gallery links
link_matches = list(re.finditer(r'<a[^>]+href=["\']([^"\']*galeria[^"\']*)["\']', html, re.IGNORECASE))
print(f"\nFound {len(link_matches)} gallery links")
for m in link_matches[:10]:
    print("  LINK:", m.group(1))

# Let's dump 2000 chars from the first gallery-looking block
first_col = html.find('col-xs-12 col-md-4')
if first_col != -1:
    print("\n=== FIRST BLOCK (col-xs-12 col-md-4) ===")
    print(html[first_col-50:first_col+1500])
else:
    # Try another pattern
    first_col = html.find('col-md-4')
    if first_col != -1:
        print("\n=== FIRST BLOCK (col-md-4) ===")
        print(html[first_col-50:first_col+1500])
    else:
        # Just dump body content
        body = html.find('<body')
        if body != -1:
            print("\n=== BODY START ===")
            print(html[body:body+3000])
