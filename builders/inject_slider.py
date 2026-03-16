import json
import re

with open('../data/events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

# Mock some dates and locations
dates = [
    "20 Mar 2026", "25 Mar 2026", "02 Abr 2026", "10 Abr 2026", "15 Abr 2026",
    "22 Abr 2026", "05 May 2026", "12 May 2026", "18 May 2026", "25 May 2026"
]
locations = [
    "Sede Central", "Centro Simón Bolívar", "Auditorio Nacional", "Olof Palme",
    "Managua", "San Juan del Sur", "Estelí", "León", "Masaya", "Granada"
]

slides_html = ""
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

    # We want a single-row date format
    # "cambiar el formato de la fecha para que se muestre en una sola fila"
    card_html = f'''
          <div class="swiper-slide h-auto">
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
    slides_html += card_html

swiper_block = f'''
        <!-- CONTENEDOR TIPO SLIDER DE EVENTOS -->
        <div class="swiper-container eventos-swiper" style="position: relative; padding-bottom: 40px; margin-top: 10px;">
          <div class="swiper-wrapper">
{slides_html}
          </div>
          <!-- Paginación del Swiper -->
          <div class="swiper-pagination eventos-pagination" style="bottom: 0px;"></div>
        </div>
'''

with open('../index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Current events are in <div class="row g-4"> ... </div> right after the title
# Let's find the section header
#             <h6 class="section-badge mb-0" style="background: linear-gradient(135deg, #0d6efd 0%, #3b82f6 100%);">
#               <i class="bi-calendar-event me-2"></i> PRÓXIMOS EVENTOS
#             </h6>
#           </div>
#           <div class="col-md-3 text-md-end text-start mt-2 mt-md-0">
#             <a href="eventos.html" class="text-decoration-none fw-bold" style="color: #0d6efd;">
#               Ver todos los eventos <i class="bi-arrow-right"></i>
#             </a>
#           </div>
#         </div>

# ... -> then `<div class="row g-4">` -> `</div>`

pattern = r'(Ver todos los eventos\s*<i class="bi-arrow-right"></i>\s*</a>\s*</div>\s*</div>).*?(<div class="row align-items-center mb-4 position-relative z-1">)'
match = re.search(pattern, text, re.DOTALL)
if match:
    # We replace everything between those two groups with our swiper block + closing tags for unified-container
    replacement = match.group(1) + "\n\n" + swiper_block + "\n      </div>\n      <div class=\"unified-container\">\n" + match.group(2)
    text = text[:match.start()] + replacement + text[match.end():]
    
    # We also need to add JS initialization for eventos-swiper at the bottom of index.html
    # We can append it just before </body>
    init_script = """
  <!-- Swiper Eventos -->
  <script>
    $(document).ready(function () {
      var eventosSwiper = new Swiper('.eventos-swiper', {
        slidesPerView: 4,
        spaceBetween: 24,
        loop: true,
        autoplay: {
            delay: 3500,
            disableOnInteraction: false,
        },
        pagination: {
          el: '.eventos-pagination',
          clickable: true,
        },
        breakpoints: {
          320: { slidesPerView: 1, spaceBetween: 15 },
          768: { slidesPerView: 2, spaceBetween: 20 },
          992: { slidesPerView: 3, spaceBetween: 24 },
          1200: { slidesPerView: 4, spaceBetween: 24 }
        }
      });
      
      // Add hover pause effect
      document.querySelector('.eventos-swiper').addEventListener('mouseenter', () => eventosSwiper.autoplay.stop());
      document.querySelector('.eventos-swiper').addEventListener('mouseleave', () => eventosSwiper.autoplay.start());
    });
  </script>
"""
    if "eventosSwiper" not in text:
        text = text.replace('</body>', init_script + '\n</body>')

    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Events slider generated successfully in index.html")
else:
    print("Eventos block pattern not found in index.html!")
