import urllib.request
import ssl
import re
import json
import time
import html as html_module

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
BASE = "https://www.tecnacional.edu.ni"

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        return response.read().decode('utf-8')

def clean_html(text):
    """Remove HTML tags and decode entities"""
    text = re.sub(r'<[^>]+>', '', text)
    text = html_module.unescape(text)
    return text.strip()

# =========================================================
# STEP 1: Get all center URLs
# =========================================================
print("=== STEP 1: Getting center list ===")
html = fetch(BASE + "/centros-tecnologicos/")
center_urls = []
for m in re.finditer(r'href=["\'](/centro/[^"\']+/)["\']', html):
    link = m.group(1)
    if link not in center_urls:
        center_urls.append(link)

print(f"Found {len(center_urls)} centers")

# =========================================================
# STEP 2: Scrape each center's detail page
# =========================================================
print("\n=== STEP 2: Scraping center details ===")
centers = []
for i, url in enumerate(center_urls):
    try:
        full_url = BASE + url
        page = fetch(full_url)
        
        # Extract center name from the URL or page title
        slug = url.strip('/').split('/')[-1]
        
        # Title from <title> tag
        title_m = re.search(r'<title>(.*?)</title>', page, re.DOTALL)
        title = clean_html(title_m.group(1)) if title_m else slug.replace('-', ' ').title()
        title = title.replace('| Tecnológico Nacional', '').replace('|', '').strip()
        
        # Description - from the "ACERCA DE" section
        desc = ""
        desc_m = re.search(r'<h1>.*?ACERCA DE.*?</h1>\s*(.*?)(?:<h\d|<div class="sidebar|<ul class="nav)', page, re.DOTALL | re.IGNORECASE)
        if desc_m:
            desc = clean_html(desc_m.group(1))
        if not desc:
            # Try alternative pattern
            desc_m = re.search(r'<p>\s*<p>(.*?)</p>', page, re.DOTALL)
            if desc_m:
                desc = clean_html(desc_m.group(1))
        
        # Image
        img = ""
        img_m = re.search(r'<img[^>]+src=["\']([^"\']*(?:centro|portada|banner)[^"\']*)["\']', page, re.IGNORECASE)
        if img_m:
            img = img_m.group(1)
            if img.startswith('/'): img = BASE + img
        else:
            # Try any image in main content
            img_m = re.search(r'<img[^>]+src=["\'](/media/[^"\']+)["\']', page)
            if img_m:
                img = BASE + img_m.group(1)
        
        # Location/Department - try to extract from content
        location = ""
        loc_m = re.search(r'(?:ubicado|departamento|ciudad|municipio)[^.]*?(?:de|en)\s+([^.,<]+)', desc, re.IGNORECASE)
        if loc_m:
            location = loc_m.group(1).strip()
        
        # Phone
        phone = ""
        phone_m = re.search(r'(?:tel[eé]fono|tel\.|llamar)[:\s]*([0-9\s\-\+\(\)]+)', page, re.IGNORECASE)
        if phone_m:
            phone = phone_m.group(1).strip()
        
        # Email
        email = ""
        email_m = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', page)
        if email_m:
            email = email_m.group(0)
        
        # Now fetch careers for this center
        careers = []
        try:
            careers_url = BASE + url + "carreras/"
            careers_page = fetch(careers_url)
            
            # Parse career entries
            for cm in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>\s*([^<]+)\s*</a>', careers_page):
                career_url = cm.group(1)
                career_name = clean_html(cm.group(2))
                if '/educacion-tecnica/' in career_url and career_name and len(career_name) > 3:
                    if career_url.startswith('/'):
                        career_url = BASE + career_url
                    careers.append({
                        'name': career_name,
                        'url': career_url
                    })
        except:
            pass
        
        center = {
            'slug': slug,
            'url': url,
            'title': title,
            'description': desc[:500] if desc else "",
            'image': img,
            'location': location,
            'phone': phone,
            'email': email,
            'careers': careers
        }
        centers.append(center)
        
        print(f"  [{i+1}/{len(center_urls)}] {title[:50]} - {len(careers)} careers")
        time.sleep(0.3)  # Be polite
        
    except Exception as e:
        print(f"  [{i+1}/{len(center_urls)}] ERROR on {url}: {e}")
        centers.append({
            'slug': url.strip('/').split('/')[-1],
            'url': url,
            'title': url.strip('/').split('/')[-1].replace('-', ' ').title(),
            'description': '',
            'image': '',
            'location': '',
            'phone': '',
            'email': '',
            'careers': []
        })

# Save
with open('../data/centers.json', 'w', encoding='utf-8') as f:
    json.dump(centers, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(centers)} centers to centers.json")
total_careers = sum(len(c['careers']) for c in centers)
print(f"Total careers across all centers: {total_careers}")
