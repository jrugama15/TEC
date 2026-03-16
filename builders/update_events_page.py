import json
import re

with open('../data/events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

dates = [
    "20 Mar 2026", "25 Mar 2026", "02 Abr 2026", "10 Abr 2026", "15 Abr 2026",
    "22 Abr 2026", "05 May 2026", "12 May 2026", "18 May 2026", "25 May 2026"
]
locations = [
    "Sede Central", "Centro Simón Bolívar", "Auditorio Nacional", "Olof Palme",
    "Managua", "San Juan del Sur", "Estelí", "León", "Masaya", "Granada"
]

cards_html = ""
for i, ev in enumerate(events[:10]):
    img_url = ev.get('image', '')
    if img_url.startswith('/'):
        img_url = 'https://www.tecnacional.edu.ni' + img_url
        
    event_url = ev.get('url', '')
    if event_url.startswith('/'):
        event_url = 'https://www.tecnacional.edu.ni' + event_url
        
    title = ev.get('title', f'Evento {i+1}')
    date_str = dates[i % len(dates)]
    loc_str = locations[i % len(locations)]

    # We want a single-row date format for eventos.html grid too
    cards_html += f'''
          <div class="col-md-4 col-lg-3">
            <div class="card event-card h-100 border-0 shadow-sm" style="border-radius: 16px; overflow: hidden; transition: transform 0.3s; background-color: #ffffff;">
              <a href="{event_url}" target="_blank" class="text-decoration-none">
                  <div style="position: relative; height: 180px; overflow: hidden;">
                    <img src="{img_url}" class="card-img-top w-100 h-100" alt="{title}" style="object-fit: cover; transition: transform 0.4s;">
                    <!-- Badge on top of image -->
                    <span style="position: absolute; top: 12px; right: 12px; background: rgba(13,110,253,0.9); color: #fff; font-size: 11px; font-weight: 800; border-radius: 6px; padding: 4px 10px; backdrop-filter: blur(4px);">EVENTO</span>
                  </div>
              </a>
              <div class="card-body p-4 d-flex flex-column">
                <div class="d-flex align-items-center mb-2" style="color: #0d6efd; font-size: 0.85rem; font-weight: 700;">
                    <i class="bi-calendar-event me-2"></i> {date_str}
                </div>
                <a href="{event_url}" target="_blank" class="text-decoration-none focus-ring">
                    <h5 class="fw-bold mb-3" style="color: #1e293b; font-size: 1.05rem; line-height: 1.4; transition: color 0.3s;">{title}</h5>
                </a>
                <p class="text-muted small mt-auto mb-0"><i class="bi-geo-alt-fill text-primary me-1"></i> {loc_str}</p>
              </div>
            </div>
          </div>
'''

with open('../pages/eventos.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace inner HTML of <div class="row g-4 mt-1"> or similar in eventos.html
pattern = r'(<div class="row g-4[^>]*>).*?(</div>\s*<!-- Pagination -->)'
match = re.search(pattern, text, re.DOTALL)
if match:
    replacement = match.group(1) + "\n" + cards_html + "\n        " + match.group(2)
    text = text[:match.start()] + replacement + text[match.end():]
    
    with open('../pages/eventos.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Events grid updated successfully in eventos.html")
else:
    print("Events grid pattern not found in eventos.html!")
