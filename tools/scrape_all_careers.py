import urllib.request
import ssl
import re
import json
import html as html_module
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
BASE = "https://www.tecnacional.edu.ni"

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        return response.read().decode('utf-8')

def clean(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = html_module.unescape(text)
    return ' '.join(text.split()).strip()

sectors_config = {
    'industria': [
        {'id': '6', 'name': 'Automotriz'},
        {'id': '18', 'name': 'Construcción'},
        {'id': '28', 'name': 'Cuero y Calzado'},
        {'id': '7', 'name': 'Electricidad y Electrónica'},
        {'id': '8', 'name': 'Energías Renovables'},
        {'id': '21', 'name': 'Madera Mueble'},
        {'id': '9', 'name': 'Metal mecánica'},
        {'id': '20', 'name': 'Pesca'},
        {'id': '27', 'name': 'Química'},
        {'id': '19', 'name': 'Refrigeración'},
        {'id': '14', 'name': 'Textil-Vestuario'},
    ],
    'comercio': [
        {'id': '4', 'name': 'Actividades Físicas y Deportivas'},
        {'id': '3', 'name': 'Administración'},
        {'id': '10', 'name': 'Docencia'},
        {'id': '13', 'name': 'Finanzas'},
        {'id': '2', 'name': 'Hotelería y Turismo'},
        {'id': '12', 'name': 'Informática'},
    ],
    'agropecuario': [
        {'id': '5', 'name': 'Agroindustria de los Alimentos'},
        {'id': '15', 'name': 'Agropecuaria'},
        {'id': '17', 'name': 'Forestal'},
        {'id': '16', 'name': 'Veterinaria'},
    ]
}

all_careers = []

for macro_sector, sectors in sectors_config.items():
    print(f"\n=== {macro_sector.upper()} ===")
    for sector in sectors:
        try:
            url = f"{BASE}/educacion-tecnica/{sector['id']}"
            page = fetch(url)
            
            # Find career links: /educacion-tecnica/SECTOR_ID/CAREER_ID
            career_links = re.findall(rf'href=["\'](/educacion-tecnica/{sector["id"]}/(\d+))["\']', page)
            unique_links = list(set(career_links))
            
            # For each link, also try to find the associated title from the page
            for link, career_id in unique_links:
                # Find the title near this link
                pattern = rf'<a[^>]+href=["\']{re.escape(link)}["\'][^>]*>(.*?)</a>'
                title_m = re.search(pattern, page, re.DOTALL)
                name = clean(title_m.group(1)) if title_m else f"Carrera {career_id}"
                
                # Find associated image
                # Look backward from the link position for an img
                link_idx = page.find(link)
                block_start = max(0, link_idx - 500)
                block = page[block_start:link_idx + 200]
                img_m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', block)
                img = ""
                if img_m:
                    img = img_m.group(1)
                    if img.startswith('/'): img = BASE + img
                
                # Find description near the link
                desc_block = page[link_idx:link_idx + 500]
                desc_m = re.search(r'<p>(.*?)</p>', desc_block, re.DOTALL)
                desc = clean(desc_m.group(1)) if desc_m else ""
                
                all_careers.append({
                    'name': name,
                    'url': BASE + link,
                    'image': img,
                    'description': desc[:300],
                    'sector_id': sector['id'],
                    'career_id': career_id,
                    'sector_name': sector['name'],
                    'macro_sector': macro_sector
                })
            
            print(f"  [{sector['id']}] {sector['name']}: {len(unique_links)} careers")
            time.sleep(0.2)
            
        except Exception as e:
            print(f"  [{sector['id']}] {sector['name']}: ERROR - {e}")

print(f"\n=== TOTAL: {len(all_careers)} careers found ===")

# Now fetch detail pages for each career
print(f"\n=== FETCHING CAREER DETAILS ===")
for i, career in enumerate(all_careers):
    try:
        page = fetch(career['url'])
        
        # Full description
        desc_m = re.search(r'<div class="info">\s*(.*?)\s*</div>', page, re.DOTALL)
        if desc_m:
            full_desc = clean(desc_m.group(1))
            if full_desc:
                career['description'] = full_desc[:800]
        
        # Try alternative description patterns
        if not career['description']:
            desc_m = re.search(r'paneles">(.*?)<div class="sidebar"', page, re.DOTALL)
            if desc_m:
                career['description'] = clean(desc_m.group(1))[:800]
        
        # Image from detail page
        if not career['image']:
            img_m = re.search(r'<img[^>]+src=["\'](/media/[^"\']+)["\']', page)
            if img_m:
                career['image'] = BASE + img_m.group(1)
        
        # Duration
        dur_m = re.search(r'(?:duraci[oó]n|dura)\s*:?\s*(\d+)\s*(meses?|a[nñ]os?|semestres?|horas?)', page, re.IGNORECASE)
        career['duration'] = f"{dur_m.group(1)} {dur_m.group(2)}" if dur_m else ""
        
        # Level
        level = ""
        title_lower = career['name'].lower()
        if 'bachillerato' in title_lower:
            level = "Bachillerato Técnico"
        elif 'especialista' in title_lower:
            level = "Técnico Especialista"
        elif 'general' in title_lower:
            level = "Técnico General"
        career['level'] = level
        
        # Modules 
        modules = []
        # Look for table rows or list items in the plan de estudios area
        plan_section = page.find('plan de estudio')
        if plan_section == -1:
            plan_section = page.find('Plan de Estudio')
        if plan_section != -1:
            plan_block = page[plan_section:plan_section+3000]
            for mod_m in re.finditer(r'<td[^>]*>(.*?)</td>', plan_block, re.DOTALL):
                mod = clean(mod_m.group(1))
                if mod and len(mod) > 3 and not mod.isdigit():
                    modules.append(mod)
        career['modules'] = modules[:30]
        
        if (i+1) % 10 == 0:
            print(f"  [{i+1}/{len(all_careers)}] Done")
        time.sleep(0.2)
        
    except Exception as e:
        career['duration'] = ""
        career['level'] = ""
        career['modules'] = []

# Save
with open('../data/careers.json', 'w', encoding='utf-8') as f:
    json.dump(all_careers, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(all_careers)} careers to careers.json")
for ms in ['industria', 'comercio', 'agropecuario']:
    count = len([c for c in all_careers if c['macro_sector'] == ms])
    print(f"  {ms}: {count} careers")
