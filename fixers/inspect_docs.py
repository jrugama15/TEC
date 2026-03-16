import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.tecnacional.edu.ni/documentos/"
try:
    with urllib.request.urlopen(url, context=ctx) as response:
        html = response.read().decode('utf-8')
        
    print(f"Fetched {len(html)} bytes.")
    
    # We want to find images and titles of documents
    # Look for card structures or <div class="col...">... 
    for match in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', html):
        src = match.group(1)
        if 'media' in src or 'document' in src or 'upload' in src:
            print(src)

    print("--- Let's look at anchor tags containing 'document' or 'media' ---")
    for match in re.finditer(r'<a.*?href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL):
        href = match.group(1)
        content = match.group(2)
        if '/media/' in href or '/documentos/' in href:
            print("URL:", href)
            # Find img inside
            img_m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
            if img_m:
                print("  IMG:", img_m.group(1))

except Exception as e:
    print("Error:", e)
