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


# Wait! In the previous inspect_docs.py, the regex was:
# for match in re.finditer(r'<a.*?href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL):
# Maybe the image is not inside the a tag but rather a tag is inside a div, and the img is somewhere else?
# Let's see the old parsing logic from inspect_docs.py

matches = re.finditer(r'<a.*?href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL)
count = 0
for match in matches:
    href = match.group(1)
    content = match.group(2)
    if '/media/' in href and 'ADAPTACION_AL' in href:
        print("CONTENT:")
        print(content)
        break
