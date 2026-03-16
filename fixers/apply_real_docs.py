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


documents = []
blocks = html.split('<div class="col-xs-12 col-md-4 wow fadeIn"')
for b in blocks[1:]:
    # extract URL
    url_match = re.search(r'href=["\']([^"\']+)["\']', b)
    if not url_match: continue
    doc_url = url_match.group(1)
    if doc_url.startswith('/'): doc_url = "https://www.tecnacional.edu.ni" + doc_url
    if 'media/.' in doc_url:
        doc_url = doc_url.replace('/media/.', '/media')
        
    # extract Img
    img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', b)
    if img_match:
        img_src = img_match.group(1)
        if img_src.startswith('/'): img_src = "https://www.tecnacional.edu.ni" + img_src
    else:
        img_src = "https://www.tecnacional.edu.ni/media/document.png.280x170_q85_crop-top.png"
        
    # extract title
    title_match = re.search(r'<p class="text-titulo"[^>]*>(.*?)</p>', b, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Documento"
    
    # extract date
    date_match = re.search(r'<p style="font-weight: bold;[^>]*>(.*?)</p>', b, re.DOTALL)
    date = date_match.group(1).strip() if date_match else "Reciente"
    
    documents.append({
        'url': doc_url,
        'image': img_src,
        'title': title,
        'date': date
    })
    
    if len(documents) == 5:
        break

cards_html = ""
for doc in documents:
    title_short = doc['title']
    if len(title_short) > 65:
        title_short = title_short[:65] + "..."
    cards_html += f'''
          <div class="col-md">
            <div class="card event-card h-100 border-0 shadow-sm" style="border-radius: 16px; overflow: hidden; background-color: #ffffff;">
              <a href="{doc['url']}" target="_blank" class="text-decoration-none">
                <div style="height: 140px; background: #fffcf8; display: flex; align-items: center; justify-content: center; overflow: hidden; position: relative;">
                  <img src="{doc['image']}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                  <i class="bi-file-earmark-pdf-fill text-danger display-4" style="display: none;"></i>
                </div>
              </a>
              <div class="card-body p-3 d-flex flex-column">
                <div class="mb-2 text-muted" style="font-size: 0.75rem;"><i class="bi-calendar-event me-1"></i> {doc['date']}</div>
                <a href="{doc['url']}" target="_blank" class="text-decoration-none focus-ring">
                  <h6 class="fw-bold mb-2" style="color: #1e293b; font-size: 0.95rem; line-height: 1.3;">{title_short}</h6>
                </a>
              </div>
            </div>
          </div>'''

with open('../index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'(<!-- SECCION MULTIMEDIA -->.*?<div class="row g-4">).*?(</div>\s*</div>\s*<!-- SECCION GALERIA DESTACADA -->)'
match = re.search(pattern, text, re.DOTALL)
if match:
    new_text = text[:match.start()] + match.group(1) + "\n" + cards_html + "\n        " + match.group(2) + text[match.end():]
    with open('../index.html', 'w', encoding='utf-8') as f:
         f.write(new_text)
    print("Replaced successfully in index.html with real scraped images!")
else:
    print("Could not find multimedia section block!")

