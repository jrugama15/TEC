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

page = fetch(BASE + "/educacion-tecnica/6")

# Find any link to /educacion-tecnica/6/NUMBER
links = re.findall(r'href=["\'](/educacion-tecnica/6/\d+)["\']', page)
print(f"Career links: {len(links)}")
for l in links:
    print(f"  {l}")

# Find any <td> or <tr> elements (tabular)
tables = page.count('<table')
print(f"\nTables: {tables}")

# Find accordion or list-group elements
for p in ['accordion', 'list-group', 'panel', 'collapse', 'ofertas', 'carreras-list', 'lista']:
    idx = page.find(p)
    if idx != -1:
        print(f"\n'{p}' found at {idx}:")
        print(page[max(0,idx-100):idx+600])
        break

# Let's find the main content more broadly
idx = page.find('ofertas-academicas')
if idx != -1:
    print(f"\n=== ofertas-academicas section ===")
    print(page[idx:idx+3000])
