import re
import json

with open("../temp/eventos_scraped.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's find all event blocks.
# Usually it's a structure with <div>... <img ...> ... <h4><a href="...">...</a></h4>...
events = []

# Try to find all <div class="col-eventos" or something similar or <div class="item">
# Let's just find each <li> or <div> that contains the image and h4.
matches = re.finditer(r'<img[^>]+src=["\']([^"\']+\.jpg[^"\']*)["\'][^>]*>.*?<h4[^>]*>\s*<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>\s*</h4>.*?<p>\s*(.*?)\s*</p>', text, re.DOTALL | re.IGNORECASE)

for m in matches:
    img = m.group(1)
    url = m.group(2)
    title = m.group(3).strip()
    date_loc = m.group(4).strip()
    
    # Prefix host if needed
    if not img.startswith('http'):
        img = "https://www.tecnacional.edu.ni" + img
    if not url.startswith('http'):
        url = "https://www.tecnacional.edu.ni" + url
        
    # Clean up tags in title or date
    title = re.sub(r'<[^>]+>', '', title)
    date_loc = re.sub(r'<[^>]+>', ' ', date_loc).strip()
    date_loc = re.sub(r'\s+', ' ', date_loc)
    
    events.append({
        'title': title,
        'image': img,
        'url': url,
        'date_loc': date_loc
    })

print(f"Found {len(events)} events!")
with open("../data/events.json", "w", encoding="utf-8") as f:
    json.dump(events[:10], f, ensure_ascii=False, indent=2)
