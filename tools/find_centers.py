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

# Try various URL patterns
urls_to_try = [
    "/centros/", "/centros", "/centro/", "/centro",
    "/centros-tecnologicos/", "/centros-tecnologicos",
]

for u in urls_to_try:
    try:
        html = fetch(BASE + u)
        print(f"SUCCESS: {u} -> {len(html)} bytes")
        # Check for center links
        links = re.findall(r'href=["\'](/centro/[^"\']+)["\']', html)
        print(f"  Center links found: {len(links)}")
        if links:
            for l in links[:5]:
                print(f"    {l}")
        break
    except Exception as e:
        print(f"FAIL: {u} -> {e}")

# Also check the example URL directly
print("\n--- Testing example center URL ---")
try:
    ex = fetch(BASE + "/centro/centro-tecnologico-alcides-miranda-fitoria/")
    print(f"Example center page: {len(ex)} bytes")
    # Extract some structure
    idx = ex.find('<h1')
    if idx != -1:
        print(ex[idx:idx+300])
    
    # Find carreras section
    idx2 = ex.find('carrera')
    if idx2 == -1:
        idx2 = ex.find('Carrera')
    if idx2 != -1:
        print("\n--- Carreras section ---")
        print(ex[max(0,idx2-200):idx2+500])
except Exception as e:
    print(f"Error: {e}")
