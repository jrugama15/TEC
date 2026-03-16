import re
import urllib.request
import ssl
import json

def fetch_centros():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # 1. First load the page
    url = 'https://www.tecnacional.edu.ni/centros-tecnologicos/'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = ""
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print("Error fetching:", e)
        return

    # Extract departments
    deps_match = re.search(r'<select[^>]*id="id_departamento"[^>]*>(.*?)</select>', html, re.DOTALL | re.IGNORECASE)
    deps_dict = {}
    if deps_match:
        opts = re.findall(r'<option value="(\d+)">([^<]+)</option>', deps_match.group(1))
        for val, name in opts:
            deps_dict[val] = name.strip()
    
    print("Found deps:", len(deps_dict))
    
    # Extract municipalities
    muns_match = re.search(r'<select[^>]*id="id_municipio"[^>]*>(.*?)</select>', html, re.DOTALL | re.IGNORECASE)
    muns_dict = {} # we can't directly map mun_id to dep_id from the HTML without API or JavaScript var
    
    # Wait, the page has this structure:
    # <div class="card" ... data-departamento="16" data-municipio="60"> 
    # Let's see if the cards contain both name, url, location, and IDs
    # Then we can just build the entire JSON structure from the cards perfectly!
    cards = re.findall(r'<div class="col-xs-12 col-md-3 mt-4"[^>]*data-departamento="(\d+)"[^>]*data-municipio="(\d+)"[^>]*>.*?<a href="([^"]+)"[^>]*>(.*?)</a>.*?<p class="card-text"><i[^>]*></i>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
    
    if not cards:
        # Maybe data attributes are on different tags
        # Let's do a wider search for any data-departamento="..."
        all_centers_info = re.findall(r'data-departamento="(\d+)".*?data-municipio="(\d+)".*?<a href="([^"]+)".*?>(.*?)</a>.*?(?:<p class="card-text">.*?(?:</i>)?(.*?)</p>)?', html, re.DOTALL | re.IGNORECASE)
        print("Using wide search")
        cards = all_centers_info

    # We need Municipio names, from the muns_match
    muns_names = {}
    if muns_match:
        opts = re.findall(r'<option value="(\d+)">([^<]+)</option>', muns_match.group(1))
        for val, name in opts:
            muns_names[val] = name.strip()

    full_data = {}
    
    for c in cards:
        dep_id = c[0]
        mun_id = c[1]
        url = c[2].strip()
        name = re.sub(r'<[^>]+>', '', c[3]).strip()
        location_raw = c[4].strip() if len(c) > 4 else ''
        
        dep_name = deps_dict.get(dep_id, f"Dep {dep_id}")
        mun_name = muns_names.get(mun_id, f"Mun {mun_id}")
        
        if dep_name not in full_data:
            full_data[dep_name] = {}
        
        if mun_name not in full_data[dep_name]:
            full_data[dep_name][mun_name] = []
            
        full_data[dep_name][mun_name].append({
            "name": name,
            "url": "https://www.tecnacional.edu.ni" + url if url.startswith('/') else url,
            "address": location_raw
        })

    # Save to a JS file
    js_content = "const nestedCentersData = " + json.dumps(full_data, ensure_ascii=False, indent=2) + ";"
    with open('centers_nested_data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("Saved {} departments with their municipalities and centers.".format(len(full_data)))
    
if __name__ == "__main__":
    fetch_centros()
