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

# Fetch Automotriz (sector 6) 
page = fetch(BASE + "/educacion-tecnica/6")
print(f"Page: {len(page)} bytes")

# Dump a chunk of the page content to see the structure
body = page.find('<body')
content = page.find('carrera')
if content == -1:
    content = page.find('lista')
if content == -1:
    content = page.find('Automotr')

print(f"\nContent at index {content}:")
if content != -1:
    print(page[max(0,content-300):content+2000])
