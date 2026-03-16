import re
import json

with open("../temp/eventos_scraped.html", "r", encoding="utf-8") as f:
    text = f.read()

images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', text)
for img in images[:10]:
    print('IMG:', img)

headers = re.findall(r'<h4[^>]*>(.*?)</h4>', text, re.DOTALL)
for h in headers[:5]:
    print('H4:', h.strip())
    
print("-" * 50)
headers3 = re.findall(r'<h3[^>]*>(.*?)</h3>', text, re.DOTALL)
for h in headers3[:5]:
    print('H3:', h.strip())
    
print("-" * 50)
headers5 = re.findall(r'<h5[^>]*>(.*?)</h5>', text, re.DOTALL)
for h in headers5[:5]:
    print('H5:', h.strip())
    
print("-" * 50)
articles = re.findall(r'<article[^>]*>(.*?)</article>', text, re.DOTALL)
for a in articles[:1]:
    print('ARTICLES:', a.strip())
