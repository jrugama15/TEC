import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.tecnacional.edu.ni/galerias/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as response:
    html = response.read().decode('utf-8')

# Find the gallery entries - we know the links pattern
# Let's find the actual gallery card structures
idx = html.find('9no-festival')
if idx != -1:
    print("=== BLOCK AROUND FIRST GALLERY ===")
    print(html[max(0, idx-500):idx+1000])
