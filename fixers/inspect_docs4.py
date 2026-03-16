import urllib.request
import ssl
from bs4 import BeautifulSoup
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.tecnacional.edu.ni/documentos/"
try:
    with urllib.request.urlopen(url, context=ctx) as response:
        html = response.read().decode('utf-8')
        
    soup = BeautifulSoup(html, 'html.parser')
    
    docs = []
    # Let's find all images that are thumbnails of documents
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/media/' in href or '/documentos/' in href:
            if href == "/documentos/": continue
            
            img = a.find('img')
            if not img: continue
            
            img_src = img.get('src')
            if not img_src: continue
            
            # The title is usually in the sibling or inside the a tag
            # let's find the text within the a tag
            p_tags = a.find_all('p')
            title = p_tags[0].get_text(strip=True) if len(p_tags) > 0 else "Documento"
            date = p_tags[-1].get_text(strip=True) if len(p_tags) > 1 else "Publicado"
            
            docs.append({
                'url': href,
                'image': img_src,
                'title': title,
                'date': date
            })
            if len(docs) == 5:
                break
                
    print(docs)
                
except Exception as e:
    print("Error:", e)
