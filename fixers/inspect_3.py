import re
import json

with open("../temp/eventos_scraped.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's find exactly the blocks
matches = re.finditer(r'<img[^>]+src=["\']([^"\']+\.jpg[^"\']*)["\'][^>]*>.*?<h4[^>]*>\s*<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>\s*</h4>', text, re.DOTALL | re.IGNORECASE)

events = []
for i, m in enumerate(matches):
    if i >= 10: break
    img = m.group(1)
    url = m.group(2)
    title = m.group(3).strip()
    
    events.append({
        'title': title,
        'image': img,
        'url': url
    })

# The user explicitly asked to change the date format to be "una sola fila"
# Right now, in the project the date looks like:
# <div class="bg-primary text-white text-center rounded p-2 me-3" style="min-width: 60px;">
#   <span class="d-block fw-bold fs-5">15</span>
#   <span class="d-block small text-uppercase">Mar</span>
# </div>
# And we need to parse actual date for each event from the scraped html if possible. Let's try to extract date.
# Usually INATEC events have <ul class="list-unstyled"><li><i class="fa fa-calendar"></i> 15 Mar</li>...</ul> or something.
# Let's extract between the match end and the next match or end of file
date_loc_matches = re.finditer(r'<ul[^>]*>.*?<li[^>]*>.*?(\d{1,2}\s+[a-zA-Z]+(\s+\d{4})?).*?</li>', text, re.DOTALL)
# wait, actually let's dump a chunk that contains the img
match1 = re.search(r'<img[^>]+src=["\']([^"\']+\.jpg[^"\']*)["\'][^>]*>.*?(?=</article>|</div></div></div>|</div>\s*</div>)', text, re.DOTALL | re.IGNORECASE)
if match1:
    print(match1.group(0))

