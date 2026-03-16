import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
BASE = "https://www.tecnacional.edu.ni"

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        return response.read().decode('utf-8')

# Inspect the careers page of our example center
url = BASE + "/centro/centro-tecnologico-alcides-miranda-fitoria/carreras/"
page = fetch(url)
print(f"Careers page: {len(page)} bytes")

# Let's dump the content around career links
idx = page.find('carrera')
if idx == -1:
    idx = page.find('Carrera')
if idx == -1:
    idx = page.find('tecnica')

print(f"\nFirst 'carrera' at index: {idx}")

# Let's find the main content area  
body_idx = page.find('<body')
# Look for list structures
for pattern in ['list-group', 'table', 'col-md', 'card', 'panel']:
    found = page.find(pattern, body_idx)
    if found != -1:
        print(f"\n'{pattern}' found at {found}:")
        print(page[max(0,found-100):found+500])
        print("---")
        break

# Also try to find all <a> tags with education links
print("\n\n=== ALL EDUCATION LINKS ===")
for m in re.finditer(r'<a[^>]+href=["\']([^"\']*educacion[^"\']*)["\'][^>]*>(.*?)</a>', page, re.DOTALL | re.IGNORECASE):
    print(f"  {m.group(1)} -> {m.group(2).strip()[:60]}")

# Also dump a big chunk of the content
content_idx = page.find('class="content"')
if content_idx == -1:
    content_idx = page.find('class="main"')
if content_idx == -1:
    content_idx = page.find('col-md-9')
if content_idx != -1:
    print(f"\n\n=== MAIN CONTENT ===")
    print(page[content_idx:content_idx+3000])
