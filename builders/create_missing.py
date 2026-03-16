import os
import re

missing_pages = [
    ('empresas.html', 'Empresas - Tecnológico Nacional'),
    ('podcast.html', 'Podcast TEC - Tecnológico Nacional'),
    ('programas.html', 'Cursos y Estrategias - Tecnológico Nacional'),
    ('experiencia-laboral.html', 'Experiencia Laboral - Tecnológico Nacional'),
    ('calidad.html', 'Calidad - Tecnológico Nacional'),
    ('adquisiciones.html', 'Adquisiciones - Tecnológico Nacional'),
    ('congreso.html', 'Congreso Docente - Tecnológico Nacional')
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
          <p class="text-muted fs-5">Página en construcción.</p>
      </div>
  </main>
  '''
    
    with open(f'../pages/{filename}', 'w', encoding='utf-8') as f:
        f.write(page_header + body + footer)
    print(f'Created/Fixed {filename}')
