import re
with open("../temp/eventos_scraped.html", "r", encoding="utf-8") as f:
    content = f.read()

matches = re.finditer(r'<img[^>]+src="([^"]+/media/event[^"]+)"[^>]*>', content)
for m in list(matches)[:10]:
    print("IMG:", m.group(1))
    
matches = re.finditer(r'<h[3-5][^>]*>(.*?)</h[3-5]>', content, re.DOTALL)
for m in list(matches)[:10]:
    print("H:", m.group(1).strip())
