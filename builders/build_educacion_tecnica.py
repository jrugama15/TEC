import json
from collections import defaultdict

with open('../data/careers.json','r',encoding='utf-8') as f:
    careers = json.load(f)

# Read footer from eventos.html
with open('../pages/eventos.html', 'r', encoding='utf-8') as f:
    ev = f.read()
footer_start = ev.find('<footer')
footer_end = ev.find('</footer>', footer_start)
FOOTER = ev[footer_start:footer_end+9]

# Group careers
grouped = defaultdict(lambda: defaultdict(list))
for c in careers:
    grouped[c['macro_sector']][c['sector_name']].append(c)

# Sector definitions
sectors = {
    'industria': {
        'name': 'Industria y Construcción',
        'icon': 'static/core/img/oferta_icon_uno.png',
        'color': '#0a5e2a',
        'border': '#2e7d32',
        'categories': list(grouped['industria'].keys())
    },
    'comercio': {
        'name': 'Comercio y Servicios',
        'icon': 'static/core/img/oferta_icon_dos.png',
        'color': '#c2185b',
        'border': '#e91e63',
        'categories': list(grouped['comercio'].keys())
    },
    'agropecuario': {
        'name': 'Agropecuario y Forestal',
        'icon': 'static/core/img/oferta_icon_tres.png',
        'color': '#558b2f',
        'border': '#7cb342',
        'categories': list(grouped['agropecuario'].keys())
    }
}

# Build category lists with collapsible careers
def build_column(macro_key, info):
    cats_html = ""
    for cat_name in info['categories']:
        cat_careers = grouped[macro_key][cat_name]
        cat_id = macro_key + '-' + cat_name.replace(' ', '-').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n')
        cat_id = ''.join(c for c in cat_id if c.isalnum() or c == '-')
        
        # Build career list items
        career_items = ""
        for c in cat_careers:
            slug = c['sector_id'] + '-' + c['career_id']
            career_items += f'''
                  <li class="list-group-item border-0 py-2 ps-4" style="background:transparent;">
                    <a href="carreras/{slug}.html" class="text-decoration-none d-flex align-items-center gap-2" style="color:#1e293b;font-size:.88rem;transition:color .2s;">
                      <i class="bi-mortarboard-fill" style="color:{info['color']};font-size:.75rem;"></i>
                      {c['name']}
                    </a>
                  </li>'''
        
        cats_html += f'''
              <div class="category-item mb-1">
                <button class="btn btn-link text-decoration-none w-100 text-start d-flex align-items-center gap-2 py-2 px-0 category-toggle" 
                        type="button" data-bs-toggle="collapse" data-bs-target="#{cat_id}" 
                        aria-expanded="false" style="color:#0a3d6b;font-size:.92rem;font-weight:500;transition:color .2s;">
                  <i class="bi-chevron-right category-chevron" style="font-size:.7rem;transition:transform .2s;color:{info['color']};"></i>
                  {cat_name}
                </button>
                <div class="collapse" id="{cat_id}">
                  <ul class="list-group list-group-flush">
                    {career_items}
                  </ul>
                </div>
              </div>'''
    
    return f'''
          <div class="col-lg-4 mb-4">
            <div class="sector-column h-100" style="background:#fff;border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,.06);overflow:hidden;">
              <!-- Sector Header -->
              <div class="d-flex align-items-center gap-3 p-4 pb-3" style="border-bottom:3px solid {info['border']};">
                <div style="width:42px;height:42px;flex-shrink:0;">
                  <img src="{info['icon']}" alt="{info['name']}" style="width:100%;height:100%;object-fit:contain;">
                </div>
                <h5 class="fw-bold mb-0" style="color:{info['color']};font-size:1.05rem;">{info['name']}</h5>
              </div>
              <!-- Categories List -->
              <div class="p-4 pt-3">
                {cats_html}
              </div>
            </div>
          </div>'''

col_industria = build_column('industria', sectors['industria'])
col_comercio = build_column('comercio', sectors['comercio'])
col_agropecuario = build_column('agropecuario', sectors['agropecuario'])

# Also build the 3 level images section (like the original site)
level_images = '''
    <!-- Niveles de Formación -->
    <div class="row g-4 mb-5">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100" style="border-radius:16px;overflow:hidden;transition:transform .3s;">
          <img src="https://www.tecnacional.edu.ni/static/img/bachillerato_tecnico.jpg" class="card-img-top" style="height:180px;object-fit:cover;" alt="Bachillerato Técnico">
          <div class="card-body text-center p-4">
            <h5 class="fw-bold" style="color:#1e293b;">Bachillerato Técnico</h5>
            <p class="text-muted small mb-0">Formación técnica integrada con la educación secundaria</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100" style="border-radius:16px;overflow:hidden;transition:transform .3s;">
          <img src="https://www.tecnacional.edu.ni/static/img/tecnico_general.jpg" class="card-img-top" style="height:180px;object-fit:cover;" alt="Técnico General">
          <div class="card-body text-center p-4">
            <h5 class="fw-bold" style="color:#1e293b;">Técnico General</h5>
            <p class="text-muted small mb-0">Carreras técnicas con certificación profesional</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100" style="border-radius:16px;overflow:hidden;transition:transform .3s;">
          <img src="https://www.tecnacional.edu.ni/static/img/tecnico_especialista.jpg" class="card-img-top" style="height:180px;object-fit:cover;" alt="Técnico Especialista">
          <div class="card-body text-center p-4">
            <h5 class="fw-bold" style="color:#1e293b;">Técnico Especialista</h5>
            <p class="text-muted small mb-0">Especialización avanzada en áreas técnicas</p>
          </div>
        </div>
      </div>
    </div>'''

html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1" name="viewport" />
    <link href="static/core/css/bootstrap.min.css" rel="stylesheet" />
    <link href="static/core/css/base.css" rel="stylesheet" />
    <link href="static/core/css/bootstrap-icons.css" rel="stylesheet" />
    <title>Carreras de Educación Técnica - Tecnológico Nacional</title>
    <meta name="description" content="Explora las 78 carreras técnicas del Tecnológico Nacional organizadas por sector: Industria, Comercio y Agropecuario.">
    <style>
      #modern-navbar {{z-index:1030;background:linear-gradient(90deg,#0a3d6b 0%,#14578b 55%,#1a72b0 100%)!important;transition:background .4s,box-shadow .3s;box-shadow:0 4px 24px rgba(10,61,107,.45)!important}}
      #modern-navbar.scrolled{{background:linear-gradient(90deg,#072d50 0%,#0e3f6b 55%,#1260a0 100%)!important}}
      #modern-navbar .navbar-brand img{{filter:brightness(0) invert(1);transition:filter .2s,opacity .2s}}
      #modern-navbar .navbar-brand:hover img{{opacity:.85}}
      #modern-navbar .nav-link{{font-size:.82rem;font-weight:600;letter-spacing:.05em;color:rgba(255,255,255,.9)!important;padding:.5rem .7rem;position:relative;transition:color .2s}}
      #modern-navbar .nav-link::after{{content:"";position:absolute;left:50%;bottom:4px;width:0;height:2px;background:#87c440;transition:width .25s,left .25s;border-radius:2px}}
      #modern-navbar .nav-link:hover::after,#modern-navbar .nav-link.active::after{{width:70%;left:15%}}
      #modern-navbar .nav-link:hover,#modern-navbar .nav-link.active{{color:#fff!important}}
      #modern-navbar .navbar-toggler{{border:1px solid rgba(255,255,255,.4);outline:none}}
      #modern-navbar .navbar-toggler-icon{{background-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba(255,255,255,0.9)' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e")}}
      #modern-navbar .dropdown-menu{{background:rgba(10,50,90,.97);border:1px solid rgba(255,255,255,.12);border-radius:14px;box-shadow:0 12px 40px rgba(0,0,0,.35);padding:8px;min-width:240px;backdrop-filter:blur(8px);animation:dropIn .18s ease}}
      @keyframes dropIn{{from{{opacity:0;transform:translateY(-8px)}}to{{opacity:1;transform:translateY(0)}}}}
      #modern-navbar .dropdown-item{{border-radius:8px;font-size:.82rem;font-weight:600;color:rgba(220,240,255,.92);padding:8px 14px;transition:background .15s,color .15s}}
      #modern-navbar .dropdown-item:hover,#modern-navbar .dropdown-item:focus{{background:#00adee;color:#fff}}
      @media(max-width:991.98px){{#modern-navbar .navbar-collapse{{background:linear-gradient(180deg,#0e3e6b 0%,#0a2d52 100%);border-radius:0 0 16px 16px;padding:14px 18px;box-shadow:0 8px 24px rgba(0,0,0,.3)}}#modern-navbar .nav-link{{color:rgba(255,255,255,.92)!important;padding:.55rem .5rem}}#modern-navbar .nav-link:hover{{color:#87c440!important}}#modern-navbar .nav-link::after{{display:none}}#modern-navbar .dropdown-menu{{background:rgba(7,35,65,.98);border-radius:10px;border:1px solid rgba(255,255,255,.1)}}#modern-navbar .dropdown-item{{color:#c8e4ff}}#modern-navbar .dropdown-item:hover{{background:#00adee;color:#fff}}}}
      @media(min-width:992px){{.nav-item.dropdown:hover>.dropdown-menu{{display:block;margin-top:0}}}}

      /* Category toggles */
      .category-toggle:hover {{ color: #00adee !important; }}
      .category-toggle[aria-expanded="true"] .category-chevron {{
        transform: rotate(90deg);
      }}
      .category-toggle[aria-expanded="true"] {{
        font-weight: 700 !important;
      }}
      .list-group-item a:hover {{
        color: #00adee !important;
        padding-left: 4px;
      }}
      .sector-column:hover {{
        box-shadow: 0 6px 24px rgba(0,0,0,.1) !important;
      }}
      .card:hover {{
        transform: translateY(-5px);
      }}
    </style>
</head>
<body class="bg-light">
  <nav class="navbar navbar-expand-lg fixed-top" id="modern-navbar">
    <div class="container-fluid px-3 px-lg-4">
      <a class="navbar-brand d-flex align-items-center gap-2 py-1" href="index.html">
        <img src="static/core/img/Recurso 36.png" alt="Logo Gobierno" style="height:38px;width:auto;max-width:180px;object-fit:contain;" />
        <img src="static/core/img/Recurso 37.png" alt="Logo INATEC" style="height:38px;width:auto;max-width:120px;object-fit:contain;" />
      </a>
      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#modernNavbarContent">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="modernNavbarContent">
        <ul class="navbar-nav ms-auto mb-0 align-items-lg-center">
          <li class="nav-item"><a class="nav-link" href="index.html">INICIO</a></li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle active" href="oferta-academica.html" id="ofertaDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">OFERTA ACADÉMICA</a>
            <ul class="dropdown-menu shadow" aria-labelledby="ofertaDropdown">
              <li><a class="dropdown-item active" href="carreras-educacion-tecnica.html">CARRERAS DE EDUCACIÓN TÉCNICA</a></li>
              <li><a class="dropdown-item" href="/programas">CURSOS Y ESTRATEGIAS DE CAPACITACIÓN</a></li>
              <li><a class="dropdown-item" href="/experiencia-laboral">RECONOCIMIENTO A LA EXPERIENCIA LABORAL</a></li>
            </ul>
          </li>
          <li class="nav-item"><a class="nav-link" href="/centros-tecnologicos">CENTROS TECNOLÓGICOS</a></li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="empresasDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">EMPRESAS</a>
            <ul class="dropdown-menu" aria-labelledby="empresasDropdown">
              <li><a class="dropdown-item" href="/empresas/">INFORMACIÓN</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="recursosDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">RECURSOS</a>
            <ul class="dropdown-menu" aria-labelledby="recursosDropdown">
              <li><a class="dropdown-item" href="noticias.html">NOTICIAS</a></li>
              <li><a class="dropdown-item" href="eventos.html">EVENTOS</a></li>
              <li><a class="dropdown-item" href="videos.html">VIDEOS</a></li>
              <li><a class="dropdown-item" href="galeria.html">GALERÍAS</a></li>
              <li><a class="dropdown-item" href="boletines.html">BOLETÍN</a></li>
              <li><a class="dropdown-item" href="biblioteca-virtual.html">BIBLIOTECA VIRTUAL</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <section class="subpage-banner" style="margin-top:55px;width:100%;position:relative;">
    <img src="static/core/img/Construyo_mi_sueño_en_el_Tecnológico_Nacional.jpeg" alt="Banner" style="width:100%;height:auto;max-height:380px;object-fit:cover;object-position:center;" />
  </section>

  <div class="container py-5">
    <!-- Breadcrumb -->
    <nav aria-label="breadcrumb" class="mb-4">
      <ol class="breadcrumb" style="background:transparent;">
        <li class="breadcrumb-item"><a href="index.html" class="text-decoration-none" style="color:#0d6efd;">Inicio</a></li>
        <li class="breadcrumb-item"><a href="oferta-academica.html" class="text-decoration-none" style="color:#0d6efd;">Oferta Académica</a></li>
        <li class="breadcrumb-item active fw-bold" style="color:#1e293b;">Carreras de Educación Técnica</li>
      </ol>
    </nav>

    <!-- Page Title -->
    <div class="text-center mb-5">
      <h1 class="fw-bold" style="color:#0a3d6b;font-size:2.2rem;">Carreras de Educación Técnica</h1>
      <p class="text-muted mx-auto" style="max-width:650px;">Explora nuestras {len(careers)} carreras técnicas organizadas en 3 sectores económicos. Selecciona una categoría para ver las carreras disponibles.</p>
    </div>

    {level_images}

    <!-- 3-Column Sector Layout -->
    <div class="row">
      {col_industria}
      {col_comercio}
      {col_agropecuario}
    </div>
  </div>

  {FOOTER}

  <script src="static/core/js/bootstrap.bundle.min.js"></script>
  <script>
    // Auto-rotate chevrons on collapse
    document.querySelectorAll('.category-toggle').forEach(function(btn) {{
      var target = document.querySelector(btn.getAttribute('data-bs-target'));
      if (target) {{
        target.addEventListener('show.bs.collapse', function() {{
          btn.setAttribute('aria-expanded', 'true');
        }});
        target.addEventListener('hide.bs.collapse', function() {{
          btn.setAttribute('aria-expanded', 'false');
        }});
      }}
    }});
  </script>

  <div id="google_translate_element" style="display:none;"></div>
  <script>
    window.addEventListener('load', function() {{
      var s = document.createElement('script');
      s.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
      document.body.appendChild(s);
    }});
    function googleTranslateElementInit() {{
      new google.translate.TranslateElement({{ pageLanguage: 'es', autoDisplay: false }}, 'google_translate_element');
    }}
  </script>
</body>
</html>'''

with open('../pages/carreras-educacion-tecnica.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Created carreras-educacion-tecnica.html with 3-column accordion layout!")
print(f"  Industria: {len(sectors['industria']['categories'])} categories")
print(f"  Comercio: {len(sectors['comercio']['categories'])} categories")
print(f"  Agropecuario: {len(sectors['agropecuario']['categories'])} categories")
print(f"  Total careers: {len(careers)}")
