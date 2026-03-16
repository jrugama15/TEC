import os
import re
import glob

# 1. Update correct Social Media links in ALL pages 
# INATEC links:
# Facebook: https://www.facebook.com/TecNacional/
# Twitter (X): https://twitter.com/TecNacional
# Instagram: https://www.instagram.com/tecnacional/
# Tiktok: https://www.tiktok.com/@tecnacional
# Linkedin: https://www.linkedin.com/company/tecnacional/
# YouTube: https://www.youtube.com/c/TecNacional

social_old = r'<ul class="icons_redes_sociales">.*?</ul>'
social_new = '''<ul class="icons_redes_sociales d-flex gap-3 justify-content-center list-unstyled mb-0 mt-3 align-items-center">
    <li title="Facebook"><a href="https://www.facebook.com/TecNacional/" target="_blank" class="text-white fs-4"><i class="bi-facebook"></i></a></li>
    <li title="Twitter"><a href="https://twitter.com/TecNacional" target="_blank" class="text-white fs-4"><i class="bi-twitter"></i></a></li>
    <li title="Instagram"><a href="https://www.instagram.com/tecnacional/" target="_blank" class="text-white fs-4"><i class="bi-instagram"></i></a></li>
    <li title="YouTube"><a href="https://www.youtube.com/c/TecNacional" target="_blank" class="text-white fs-4"><i class="bi-youtube"></i></a></li>
    <li title="Tiktok"><a href="https://www.tiktok.com/@tecnacional" target="_blank" class="text-white fs-4"><i class="bi-tiktok"></i></a></li>
</ul>'''

all_files = glob.glob('../pages/*.html') + ['../index.html']
for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(social_old, social_new, content, flags=re.DOTALL)
    
    # 2. Fix structure for campus-virtual.html and innovatec.html
    # These pages were generated somehow individually and lack the proper navbar/footer/head
    if 'campus-virtual.html' in filepath or 'innovatec.html' in filepath:
        # Just give them the same standard structure
        # Let's extract banner/main and re-wrap if they are custom
        # But honestly, they are just placeholders right now. 
        # I'll let another script process them.
        pass
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated social links in {filepath}")

# 3. Regenerate campus-virtual, innovatec, podcast, in create_missing
missing_pages = [
    ('campus-virtual.html', 'Campus Virtual - Tecnológico Nacional'),
    ('innovatec.html', 'INNOVATEC - Tecnológico Nacional'),
    ('podcast.html', 'Podcast TEC - Tecnológico Nacional')
]

with open('../pages/eventos.html', 'r', encoding='utf-8') as f:
    template = f.read()

start_nav = template.find('<!-- SECCION BANNER DE SUBPAGINA -->')
if start_nav == -1:
    start_nav = template.find('</nav>')
    if start_nav != -1: start_nav += 6

start_footer = template.find('<footer')

header = template[:start_nav]
footer = template[start_footer:]

for filename, title in missing_pages:
    page_header = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', header)
    
    body = f'''
  <section class="subpage-banner" style="margin-top: 55px; width: 100%; position: relative;">
      <img src="../static/core/img/Construyo_mi_sueño_en_el_Tecnológico_Nacional.jpeg" alt="Banner" style="width: 100%; height: auto; max-height: 380px; object-fit: cover; object-position: center;" />
  </section>
  <main class="container py-5 text-center" style="min-height: 50vh; display: flex; align-items: center; justify-content: center;">
      <div>
          <h1 class="fw-bold" style="color: #1e40af;">{title.split('-')[0].strip()}</h1>
          <p class="text-muted fs-5">Plataforma en construcción o en proceso de migración.</p>
          <a href="../index.html" class="btn btn-primary mt-3 rounded-pill px-4" style="background: linear-gradient(135deg, #0d6efd 0%, #00adee 100%); border: none;">Volver al Inicio</a>
      </div>
  </main>
  '''
    
    with open(f'../pages/{filename}', 'w', encoding='utf-8') as f:
        f.write(page_header + body + footer)
    print(f'Fixed structure for {filename}')
