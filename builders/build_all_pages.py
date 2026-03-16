import json
import os
import re

def clean_filename(name):
    return re.sub(r'[^\w\-]', '', name.replace(' ', '-').lower())[:80]

with open('../data/centers.json', 'r', encoding='utf-8') as f:
    centers = json.load(f)
with open('../data/careers.json', 'r', encoding='utf-8') as f:
    careers = json.load(f)

# Read template pieces from eventos.html
with open('../pages/eventos.html', 'r', encoding='utf-8') as f:
    ev = f.read()

head_start = ev.find('<head>')
head_end = ev.find('</head>')
HEAD_TAG = ev[head_start:head_end+7]
# Remove title and description from HEAD_TAG
HEAD_TAG = re.sub(r'<title>.*?</title>', '', HEAD_TAG, flags=re.DOTALL)
HEAD_TAG = re.sub(r'<meta name="description".*?>', '', HEAD_TAG, flags=re.DOTALL)

body_open = ev.find('<body class="bg-light">')
nav_start = ev.find('<style>', body_open)
nav_end = ev.find('<!-- End of modern navbar -->') + len('<!-- End of modern navbar -->')
NAVBAR = ev[nav_start:nav_end]

footer_start = ev.find('<footer')
FOOTER = ev[footer_start:]

# Fix internal page links for use in 'centros/' and 'carreras/' directories
# It will match any href that starts with a letter and ends with .html and prepends '../pages/'
FOOTER_NESTED = re.sub(r'href=\"([a-zA-Z0-9_\-]+\.html)\"', r'href="../pages/\1"', FOOTER)

# We must do the same for the NAVBAR to avoid broken dropdown links
NAVBAR_NESTED = re.sub(r'href=\"([a-zA-Z0-9_\-]+\.html)\"', r'href="../pages/\1"', NAVBAR)


# Common head
def get_head(title, desc=""):
    head = f'<!DOCTYPE html>\n<html lang="es">\n{HEAD_TAG}'
    head = head.replace('</head>', f'  <title>{title} - Tecnológico Nacional</title>\n  <meta name="description" content="{desc[:160]}">\n</head>')
    return head

# =========================================================
# CREATE CENTER MICROSITES
# =========================================================
os.makedirs('../centros', exist_ok=True)

print("=== Creating center microsites ===")
for i, center in enumerate(centers):
    slug = center['slug']
    
    # Build careers list HTML
    careers_html = ""
    if center['careers']:
        for c in center['careers']:
            c_img = c.get('image', '')
            c_name = c.get('name', 'Carrera')
            c_desc = c.get('description', '')[:120]
            
            c_slug = ""
            for gc in careers:
                if gc.get('name') == c_name:
                    c_slug = f"../carreras/{gc['sector_id']}-{gc['career_id']}.html"
                    break
            if not c_slug:
                c_slug = "../pages/carreras-educacion-tecnica.html"
                
            careers_html += f'''
            <div class="col-md-6 col-lg-4 mb-4">
              <a href="{c_slug}" class="text-decoration-none">
                <div class="card h-100 border-0 shadow-sm" style="border-radius:16px;overflow:hidden;transition:transform .3s;">
                  <div style="height:160px;overflow:hidden;background:#f0f4f8;">
                    {'<img src="' + c_img + '" class="w-100 h-100" style="object-fit:cover;" loading="lazy">' if c_img else '<div class="d-flex align-items-center justify-content-center h-100"><i class="bi-mortarboard display-3 text-primary opacity-50"></i></div>'}
                  </div>
                  <div class="card-body p-3">
                    <h6 class="fw-bold mb-2" style="color:#1e293b;font-size:.9rem;line-height:1.3;">{c_name}</h6>
                    <p class="text-muted small mb-0">{c_desc}</p>
                  </div>
                </div>
              </a>
            </div>'''
    else:
        careers_html = '<div class="col-12"><p class="text-muted text-center py-4">Información de carreras no disponible actualmente.</p></div>'

    desc = center.get('description', '').replace('"', '&quot;')
    img = center.get('image', '')
    
    page_html = f'''{get_head(center['title'], desc)}
<body class="bg-light">
  {nav_modified}

  <div class="container py-5">
    <!-- Breadcrumb -->
    <nav aria-label="breadcrumb" class="mb-4">
      <ol class="breadcrumb" style="background:transparent;">
        <li class="breadcrumb-item"><a href="../index.html" class="text-decoration-none" style="color:#0d6efd;">Inicio</a></li>
        <li class="breadcrumb-item"><a href="../pages/centros-tecnologicos.html" class="text-decoration-none" style="color:#0d6efd;">Centros Tecnológicos</a></li>
        <li class="breadcrumb-item active fw-bold" style="color:#1e293b;">{center['title'][:50]}</li>
      </ol>
    </nav>

    <!-- Center Header -->
    <div class="row mb-5">
      <div class="col-lg-{'6' if img else '12'}">
        <h6 class="d-inline-block px-4 py-2 rounded-pill fw-bold text-white mb-3" style="background:linear-gradient(135deg,#0d6efd 0%,#00adee 100%);font-size:.8rem;letter-spacing:.1em;">
          <i class="bi-building me-2"></i>CENTRO TECNOLÓGICO
        </h6>
        <h2 class="fw-bold mb-3" style="color:#1e293b;">{center['title']}</h2>
        <p class="text-muted" style="line-height:1.8;">{desc[:600]}</p>
        
        <div class="d-flex flex-wrap gap-3 mt-4">
          {f'<div class="d-flex align-items-center gap-2"><i class="bi-geo-alt-fill text-primary"></i><span class="text-muted small">{center.get("location","")}</span></div>' if center.get('location') else ''}
          {f'<div class="d-flex align-items-center gap-2"><i class="bi-telephone-fill text-primary"></i><span class="text-muted small">{center.get("phone","")}</span></div>' if center.get('phone') else ''}
          {f'<div class="d-flex align-items-center gap-2"><i class="bi-envelope-fill text-primary"></i><span class="text-muted small">{center.get("email","")}</span></div>' if center.get('email') else ''}
        </div>
      </div>
      {'<div class="col-lg-6 mt-4 mt-lg-0"><div class="rounded-4 overflow-hidden shadow-sm" style="height:300px;"><img src="' + img + '" class="w-100 h-100" style="object-fit:cover;" alt="' + center["title"][:40] + '"></div></div>' if img else ''}
    </div>

    <!-- Careers Section -->
    <div class="mb-5">
      <h4 class="fw-bold mb-4" style="color:#1e293b;">
        <i class="bi-mortarboard-fill text-primary me-2"></i>Carreras Ofertadas
        <span class="badge bg-primary rounded-pill ms-2" style="font-size:.7rem;">{len(center['careers'])}</span>
      </h4>
      <div class="row">
        {careers_html}
      </div>
    </div>

    <!-- Quick Info -->
    <div class="row g-4 mb-5">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100" style="border-radius:16px;background:linear-gradient(135deg,#e0f2fe,#bae6fd);">
          <div class="card-body text-center p-4">
            <i class="bi-people-fill display-4 text-primary mb-3"></i>
            <h5 class="fw-bold">Matrícula Abierta</h5>
            <p class="text-muted small">Consulta los requisitos de ingreso y realiza tu matrícula</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100" style="border-radius:16px;background:linear-gradient(135deg,#fef3c7,#fde68a);">
          <div class="card-body text-center p-4">
            <i class="bi-clock-fill display-4 text-warning mb-3"></i>
            <h5 class="fw-bold">Horarios Flexibles</h5>
            <p class="text-muted small">Turnos matutino, vespertino y sabatino disponibles</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100" style="border-radius:16px;background:linear-gradient(135deg,#d1fae5,#a7f3d0);">
          <div class="card-body text-center p-4">
            <i class="bi-award-fill display-4 text-success mb-3"></i>
            <h5 class="fw-bold">Certificación Oficial</h5>
            <p class="text-muted small">Título avalado por el Tecnológico Nacional</p>
          </div>
        </div>
      </div>
    </div>
  </div>

{FOOTER_NESTED}
'''

    filepath = f'../centros/{slug}.html'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page_html)
    
    if (i+1) % 10 == 0:
        print(f"  [{i+1}/{len(centers)}] centers created")

print(f"  Created {len(centers)} center microsites in centros/")

# =========================================================
# CREATE CAREER DETAIL PAGES
# =========================================================
os.makedirs('../carreras', exist_ok=True)

print("\n=== Creating career detail pages ===")
for c in careers:
    slug = f"{c['sector_id']}-{c['career_id']}"
    
    # Find which centers offer this career based on name match
    offering_centers = []
    for center in centers:
        if any(cc.get('name') == c['name'] for cc in center['careers']):
            offering_centers.append(center)
            
    centers_html = ""
    if offering_centers:
        for oc in offering_centers:
            centers_html += f'''
            <a href="../centros/{oc['slug']}.html" class="list-group-item list-group-item-action d-flex align-items-center gap-3 p-3 border-0 rounded-3 mb-2 shadow-sm" style="transition:all .2s;">
              <div class="bg-primary bg-opacity-10 p-2 rounded-circle">
                <i class="bi-building text-primary"></i>
              </div>
              <div class="flex-grow-1">
                <h6 class="mb-0 fw-bold">{oc['title']}</h6>
                <small class="text-muted"><i class="bi-geo-alt me-1"></i>{oc.get('location', '')}</small>
              </div>
              <i class="bi-chevron-right text-muted"></i>
            </a>'''
    else:
        centers_html = '<div class="alert alert-light border">No hay centros asignados actualmente para esta carrera.</div>'

    info = {
        'industria': {'color':'#14578b','icon':'bi-gear-fill'},
        'comercio':  {'color':'#00adee','icon':'bi-shop'},
        'agropecuario':{'color':'#87c440','icon':'bi-tree-fill'}
    }.get(c['sector_id'], {'color':'#6c757d','icon':'bi-bookmark-fill'})
    
    page_html = f'''{get_head(c['name'], c['description'])}
<body class="bg-light">
  {NAVBAR_NESTED.replace('../static/core/img/Construyo_mi_sueño_en_el_Tecnológico_Nacional.jpeg', (c.get('image') if c.get('image') else '../static/core/img/Construyo_mi_sueño_en_el_Tecnológico_Nacional.jpeg'))}

  <div class="container py-5">
    <!-- Breadcrumb -->
    <nav aria-label="breadcrumb" class="mb-4">
      <ol class="breadcrumb" style="background:transparent;">
        <li class="breadcrumb-item"><a href="../index.html" class="text-decoration-none" style="color:#0d6efd;">Inicio</a></li>
        <li class="breadcrumb-item"><a href="../pages/carreras-educacion-tecnica.html" class="text-decoration-none" style="color:#0d6efd;">Carreras</a></li>
        <li class="breadcrumb-item active fw-bold" style="color:#1e293b;">{c['name'][:40]}...</li>
      </ol>
    </nav>

    <!-- Career Header -->
    <div class="row align-items-center mb-5">
      <div class="col-lg-8">
        <h6 class="d-inline-flex align-items-center gap-2 px-3 py-2 rounded-pill fw-bold text-white mb-3 shadow-sm" 
            style="background:{info['color']};font-size:.8rem;letter-spacing:.05em;">
          <i class="{info['icon']}"></i>SECTOR {c['sector_id'].upper()}
        </h6>
        <h2 class="fw-bold mb-3 display-6" style="color:#1e293b;">{c['name']}</h2>
        {f'<span class="badge bg-light text-dark border p-2 px-3 fs-6 rounded-pill shadow-sm mb-4"><i class="bi-award me-2"></i>{c["level"]}</span>' if c.get('level') else ''}
      </div>
    </div>

    <div class="row g-5">
      <!-- Description -->
      <div class="col-lg-7">
        <div class="card border-0 shadow-sm p-4 p-md-5" style="border-radius:20px;">
          <h4 class="fw-bold mb-4" style="color:#1e293b;">
            <i class="bi-info-circle-fill text-primary me-2"></i>Sobre la Carrera
          </h4>
          <p class="text-muted fs-6" style="line-height:1.8;">{c['description']}</p>
        </div>
      </div>
      
      <!-- Centers list -->
      <div class="col-lg-5">
        <div class="card border-0 shadow-sm p-4" style="border-radius:20px;background:#f8fafc;">
          <h5 class="fw-bold mb-4" style="color:#1e293b;">
            <i class="bi-geo-alt-fill text-danger me-2"></i>Disponible en
            <span class="badge bg-danger rounded-pill ms-2">{len(offering_centers)}</span>
          </h5>
          <div class="list-group list-group-flush" style="max-height:500px;overflow-y:auto;">
            {centers_html}
          </div>
        </div>
      </div>
    </div>
  </div>

{FOOTER}
'''

    with open(f'../carreras/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(page_html)

print(f"  Created {len(careers)} career detail pages in carreras/")



# =========================================================
# UPDATE INDEX.HTML - center search links
# =========================================================
print("\n=== Updating index.html center links ===")
with open('../index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Build a JS data structure for the center search
centers_js = json.dumps([{
    'title': c['title'],
    'slug': c['slug'],
    'location': c.get('location', ''),
    'careers': len(c['careers'])
} for c in centers], ensure_ascii=False)

# Update menu link for education
index_html = index_html.replace('href="/educacion-tecnica"', 'href="pages/carreras-educacion-tecnica.html"')

with open('../index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("  Updated index.html")

print("\nALL DONE!")
