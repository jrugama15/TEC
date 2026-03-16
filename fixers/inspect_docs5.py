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
except Exception as e:
    print("Could not fetch documents", e)
    html = ""

matches = re.finditer(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL)
count = 0
for match in matches:
    href = match.group(1)
    content = match.group(2)
    
    if '/media/' in href:
        print("FOUND HREF:", href)
        if 'media/.' in href:
            href = href.replace('/media/.', '/media/')
        if href.startswith('/'): href = "https://www.tecnacional.edu.ni" + href
        
        img_m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
        if img_m:
            img_src = img_m.group(1)
            if img_src.startswith('/'): img_src = "https://www.tecnacional.edu.ni" + img_src
            print("FOUND IMG:", img_src)
            count += 1
            if count == 5: break
