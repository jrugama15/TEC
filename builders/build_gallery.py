import json
import re

# Load galleries data
with open('../data/galleries.json', 'r', encoding='utf-8') as f:
    galleries = json.load(f)

# Fix HTML entities in titles
for g in galleries:
    g['title'] = g['title'].replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')

# ============================================================
# PART 1: Create galeria.html page
# ============================================================

gallery_cards_html = ""
for i, g in enumerate(galleries):
    # Build image grid for each gallery
    images_grid = ""
    for j, img in enumerate(g['images']):
        images_grid += f'''
                <div class="col-6 col-md-4 col-lg-3 gallery-thumb" data-gallery="{i}" data-index="{j}">
                  <div class="position-relative overflow-hidden shadow-sm" style="border-radius: 12px; cursor: pointer; height: 180px;">
                    <img src="{img}" class="w-100 h-100" style="object-fit: cover; transition: transform 0.4s ease;" 
                         onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'" 
                         alt="{g['title']}" loading="lazy">
                    <div class="position-absolute bottom-0 start-0 w-100 p-2" style="background: linear-gradient(0deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0) 100%);">
                      <span class="text-white" style="font-size: 0.7rem;"><i class="bi-zoom-in"></i></span>
                    </div>
                  </div>
                </div>'''

    short_title = g['title'] if len(g['title']) <= 80 else g['title'][:80] + '...'
    
    gallery_cards_html += f'''
        <!-- Galería {i+1} -->
        <div class="gallery-section mb-5" id="gallery-{i}">
          <div class="d-flex align-items-center mb-3">
            <div class="me-3" style="width: 5px; height: 40px; background: linear-gradient(180deg, #a855f7, #7e22ce); border-radius: 4px;"></div>
            <h4 class="fw-bold mb-0" style="color: #1e293b; font-size: 1.2rem;">{short_title}</h4>
          </div>
          <div class="row g-3">
            {images_grid}
          </div>
        </div>'''


galeria_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1" name="viewport" />
    <link href="static/core/css/bootstrap.min.css" rel="stylesheet" />
    <link href="static/core/css/base.css" rel="stylesheet" />
    <link href="static/core/css/bootstrap-icons.css" rel="stylesheet" />
    <title>Galería - Tecnológico Nacional</title>
    <meta name="description" content="Galería fotográfica del Tecnológico Nacional INATEC. Explora eventos, inauguraciones y actividades educativas en imágenes.">
</head>
<body class="bg-light">
  <style>
    /* ── Navbar background: matches banner blue ── */
    #modern-navbar {{
      z-index: 1030;
      background: linear-gradient(90deg, #0a3d6b 0%, #14578b 55%, #1a72b0 100%) !important;
      transition: background 0.4s, box-shadow 0.3s;
      box-shadow: 0 4px 24px rgba(10,61,107,0.45) !important;
    }}
    #modern-navbar.scrolled {{
      background: linear-gradient(90deg, #072d50 0%, #0e3f6b 55%, #1260a0 100%) !important;
      box-shadow: 0 4px 24px rgba(10,61,107,0.45) !important;
    }}
    #modern-navbar .navbar-brand img {{
      filter: brightness(0) invert(1);
      transition: filter 0.2s, opacity 0.2s;
    }}
    #modern-navbar .navbar-brand:hover img {{ opacity: 0.85; }}
    #modern-navbar .nav-link {{
      font-size: 0.82rem; font-weight: 600; letter-spacing: 0.05em;
      color: rgba(255,255,255,0.9) !important; padding: 0.5rem 0.7rem;
      position: relative; transition: color 0.2s;
    }}
    #modern-navbar .nav-link::after {{
      content: ""; position: absolute; left: 50%; bottom: 4px; width: 0; height: 2px;
      background: #87c440; transition: width 0.25s, left 0.25s; border-radius: 2px;
    }}
    #modern-navbar .nav-link:hover::after,
    #modern-navbar .nav-link.active::after {{ width: 70%; left: 15%; }}
    #modern-navbar .nav-link:hover, #modern-navbar .nav-link.active {{ color: #fff !important; }}
    #modern-navbar .navbar-toggler {{
      border: 1px solid rgba(255,255,255,0.4); outline: none;
      box-shadow: 0 4px 24px rgba(10,61,107,0.45) !important;
    }}
    #modern-navbar .navbar-toggler-icon {{
      background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba(255,255,255,0.9)' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
    }}
    #modern-navbar .dropdown-menu {{
      background: rgba(10, 50, 90, 0.97); border: 1px solid rgba(255,255,255,0.12);
      border-radius: 14px; box-shadow: 0 12px 40px rgba(0,0,0,0.35); padding: 8px;
      min-width: 240px; backdrop-filter: blur(8px); animation: dropIn 0.18s ease;
    }}
    @keyframes dropIn {{ from {{ opacity: 0; transform: translateY(-8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    #modern-navbar .dropdown-item {{
      border-radius: 8px; font-size: 0.82rem; font-weight: 600;
      color: rgba(220,240,255,0.92); padding: 8px 14px; transition: background 0.15s, color 0.15s;
    }}
    #modern-navbar .dropdown-item:hover, #modern-navbar .dropdown-item:focus {{ background: #00adee; color: #fff; }}
    @media (max-width: 991.98px) {{
      #modern-navbar .navbar-collapse {{
        background: linear-gradient(180deg, #0e3e6b 0%, #0a2d52 100%);
        border-radius: 0 0 16px 16px; padding: 14px 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      }}
      #modern-navbar .nav-link {{ color: rgba(255,255,255,0.92) !important; padding: 0.55rem 0.5rem; }}
      #modern-navbar .nav-link:hover {{ color: #87c440 !important; }}
      #modern-navbar .nav-link::after {{ display: none; }}
      #modern-navbar .dropdown-menu {{
        background: rgba(7,35,65,0.98); border-radius: 10px;
        box-shadow: 0 4px 24px rgba(10,61,107,0.45) !important; border: 1px solid rgba(255,255,255,0.1);
      }}
      #modern-navbar .dropdown-item {{ color: #c8e4ff; }}
      #modern-navbar .dropdown-item:hover {{ background: #00adee; color: #fff; }}
    }}
    @media (min-width: 992px) {{
      .nav-item.dropdown:hover > .dropdown-menu {{ display: block; margin-top: 0; }}
    }}

    /* Lightbox */
    .lightbox-overlay {{
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.92); z-index: 9999; display: none;
      align-items: center; justify-content: center; flex-direction: column;
      backdrop-filter: blur(10px);
    }}
    .lightbox-overlay.active {{ display: flex; }}
    .lightbox-overlay img {{
      max-width: 90%; max-height: 80vh; border-radius: 12px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }}
    .lightbox-close {{
      position: absolute; top: 20px; right: 30px; color: #fff;
      font-size: 2rem; cursor: pointer; z-index: 10000;
      background: rgba(255,255,255,0.1); border: none; border-radius: 50%;
      width: 50px; height: 50px; display: flex; align-items: center; justify-content: center;
      transition: background 0.2s;
    }}
    .lightbox-close:hover {{ background: rgba(255,255,255,0.25); }}
    .lightbox-nav {{
      position: absolute; top: 50%; color: #fff; font-size: 2.5rem;
      cursor: pointer; transform: translateY(-50%); background: rgba(255,255,255,0.1);
      border: none; border-radius: 50%; width: 60px; height: 60px;
      display: flex; align-items: center; justify-content: center; transition: background 0.2s;
    }}
    .lightbox-nav:hover {{ background: rgba(255,255,255,0.25); }}
    .lightbox-prev {{ left: 20px; }}
    .lightbox-next {{ right: 20px; }}
    .lightbox-counter {{
      color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 15px; font-weight: 600;
    }}

    .gallery-thumb:hover img {{ transform: scale(1.08); }}
  </style>

  <nav class="navbar navbar-expand-lg fixed-top" id="modern-navbar" style="z-index:1030;">
    <div class="container-fluid px-3 px-lg-4">
      <a class="navbar-brand d-flex align-items-center gap-2 py-1" href="index.html">
        <img src="static/core/img/Recurso 36.png" alt="Logo Gobierno" style="height:38px; width:auto; max-width:180px; object-fit:contain;" />
        <img src="static/core/img/Recurso 37.png" alt="Logo INATEC" style="height:38px; width:auto; max-width:120px; object-fit:contain;" />
      </a>
      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse"
        data-bs-target="#modernNavbarContent" aria-controls="modernNavbarContent" aria-expanded="false" aria-label="Abrir menú" style="color:#14578b;">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="modernNavbarContent">
        <ul class="navbar-nav ms-auto mb-0 align-items-lg-center">
          <li class="nav-item"><a class="nav-link" href="index.html">INICIO</a></li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="oferta-academica.html" id="ofertaDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">OFERTA ACADÉMICA</a>
            <ul class="dropdown-menu shadow" aria-labelledby="ofertaDropdown">
              <li><a class="dropdown-item" href="/educacion-tecnica">CARRERAS DE EDUCACIÓN TÉCNICA</a></li>
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
              <li><a class="dropdown-item active" href="galeria.html">GALERÍAS</a></li>
              <li><a class="dropdown-item" href="boletines.html">BOLETÍN</a></li>
              <li><a class="dropdown-item" href="/recursos/calidad">CALIDAD</a></li>
              <li><a class="dropdown-item" href="/recursos/documento">ADQUISICIONES</a></li>
              <li><a class="dropdown-item" href="biblioteca-virtual.html">BIBLIOTECA VIRTUAL</a></li>
              <li><a class="dropdown-item" href="/congreso/">CONGRESO DOCENTE</a></li>
              <li><a class="dropdown-item" href="https://correo.tecnacional.edu.ni/">CORREO INSTITUCIONAL</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- SECCION BANNER DE SUBPAGINA -->
  <section class="subpage-banner" style="margin-top: 55px; width: 100%; position: relative;">
    <img src="static/core/img/Construyo_mi_sueño_en_el_Tecnológico_Nacional.jpeg" alt="Construyo mi sueño en el Tecnológico Nacional" style="width: 100%; height: auto; max-height: 380px; object-fit: cover; object-position: center;" />
  </section>

  <!-- MAIN CONTENT -->
  <div class="container py-5">
    <!-- Page Header -->
    <div class="text-center mb-5">
      <h6 class="d-inline-block px-4 py-2 rounded-pill fw-bold text-white mb-3" style="background: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%); font-size: 0.85rem; letter-spacing: 0.1em;">
        <i class="bi-camera-fill me-2"></i>GALERÍA FOTOGRÁFICA
      </h6>
      <h2 class="fw-bold" style="color: #1e293b;">Nuestros Momentos Destacados</h2>
      <p class="text-muted mx-auto" style="max-width: 600px;">Revive los eventos, inauguraciones y actividades más importantes del Tecnológico Nacional a través de nuestras galerías fotográficas.</p>
    </div>

    <!-- Gallery Navigation Pills -->
    <div class="d-flex flex-wrap gap-2 justify-content-center mb-5">
      <button class="btn btn-sm px-3 py-2 rounded-pill fw-bold gallery-filter active" data-filter="all" style="font-size: 0.8rem;">
        <i class="bi-grid-3x3-gap me-1"></i> Todas
      </button>''' + ''.join([f'''
      <button class="btn btn-sm px-3 py-2 rounded-pill fw-bold gallery-filter" data-filter="{i}" style="font-size: 0.8rem;">
        {g['title'][:30]}{'...' if len(g['title']) > 30 else ''}
      </button>''' for i, g in enumerate(galleries)]) + f'''
    </div>

    <!-- Gallery Sections -->
    {gallery_cards_html}
  </div>

  <!-- Lightbox -->
  <div class="lightbox-overlay" id="lightbox">
    <button class="lightbox-close" onclick="closeLightbox()"><i class="bi-x-lg"></i></button>
    <button class="lightbox-nav lightbox-prev" onclick="prevImage()"><i class="bi-chevron-left"></i></button>
    <button class="lightbox-nav lightbox-next" onclick="nextImage()"><i class="bi-chevron-right"></i></button>
    <img id="lightbox-img" src="" alt="Gallery image">
    <div class="lightbox-counter" id="lightbox-counter"></div>
  </div>

  <script src="static/core/js/bootstrap.bundle.min.js"></script>
  <script>
    // Gallery filter
    document.querySelectorAll('.gallery-filter').forEach(btn => {{
      btn.addEventListener('click', function() {{
        document.querySelectorAll('.gallery-filter').forEach(b => {{
          b.classList.remove('active');
          b.style.background = '';
          b.style.color = '';
        }});
        this.classList.add('active');
        this.style.background = 'linear-gradient(135deg, #a855f7, #7e22ce)';
        this.style.color = '#fff';

        const filter = this.dataset.filter;
        document.querySelectorAll('.gallery-section').forEach(section => {{
          if (filter === 'all' || section.id === 'gallery-' + filter) {{
            section.style.display = 'block';
            section.style.animation = 'fadeIn 0.4s ease';
          }} else {{
            section.style.display = 'none';
          }}
        }});
      }});
    }});

    // Initialize active state
    document.querySelector('.gallery-filter.active').style.background = 'linear-gradient(135deg, #a855f7, #7e22ce)';
    document.querySelector('.gallery-filter.active').style.color = '#fff';

    // Lightbox
    let currentImages = [];
    let currentIndex = 0;

    document.querySelectorAll('.gallery-thumb').forEach(thumb => {{
      thumb.addEventListener('click', function() {{
        const galleryId = this.dataset.gallery;
        const index = parseInt(this.dataset.index);
        currentImages = [];
        document.querySelectorAll(`.gallery-thumb[data-gallery="${{galleryId}}"]`).forEach(t => {{
          currentImages.push(t.querySelector('img').src);
        }});
        currentIndex = index;
        showLightbox();
      }});
    }});

    function showLightbox() {{
      document.getElementById('lightbox-img').src = currentImages[currentIndex];
      document.getElementById('lightbox-counter').textContent = (currentIndex + 1) + ' / ' + currentImages.length;
      document.getElementById('lightbox').classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function closeLightbox() {{
      document.getElementById('lightbox').classList.remove('active');
      document.body.style.overflow = '';
    }}

    function nextImage() {{
      currentIndex = (currentIndex + 1) % currentImages.length;
      showLightbox();
    }}

    function prevImage() {{
      currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
      showLightbox();
    }}

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {{
      if (!document.getElementById('lightbox').classList.contains('active')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowRight') nextImage();
      if (e.key === 'ArrowLeft') prevImage();
    }});

    // Click overlay to close
    document.getElementById('lightbox').addEventListener('click', function(e) {{
      if (e.target === this) closeLightbox();
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

with open('../pages/galeria.html', 'w', encoding='utf-8') as f:
    f.write(galeria_html)
print("Created galeria.html")

# ============================================================
# PART 2: Update Gallery Section on Home (index.html)  
# ============================================================
with open('../index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Build new gallery section with gradient overlay cards for all 5 galleries
# First gallery = large left, next 4 = 2x2 grid right
g0 = galleries[0]
g1 = galleries[1] if len(galleries) > 1 else galleries[0]
g2 = galleries[2] if len(galleries) > 2 else galleries[0]
g3 = galleries[3] if len(galleries) > 3 else galleries[0]
g4 = galleries[4] if len(galleries) > 4 else galleries[0]

# Use a higher quality cover for the main image
main_cover = g0['images'][0] if g0['images'] else g0['cover']

new_gallery = f'''<!-- SECCION GALERIA DESTACADA -->
      <div class="unified-container my-5">
        <div class="row align-items-center mb-4">
          <div class="col-md-9 text-start">
            <h6 class="section-badge mb-0" style="background: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%);">
              <i class="bi-camera-fill me-2"></i> GALERÍA DESTACADA
            </h6>
          </div>
          <div class="col-md-3 text-md-end text-start mt-2 mt-md-0">
            <a href="galeria.html" class="text-decoration-none fw-bold" style="color: #9333ea;">
              Ver galería <i class="bi-arrow-right"></i>
            </a>
          </div>
        </div>

        <div class="row g-3">
          <!-- Columna Izquierda: Foto Principal Grande -->
          <div class="col-lg-6">
            <a href="galeria.html#gallery-0" class="text-decoration-none">
              <div class="position-relative overflow-hidden shadow-sm" style="border-radius: 16px; height: 100%; min-height: 400px; cursor: pointer;">
                <img src="{main_cover}" class="w-100 h-100" style="object-fit: cover; transition: transform 0.5s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" alt="{g0['title'][:50]}">
                <div class="position-absolute bottom-0 start-0 w-100 p-4" style="background: linear-gradient(0deg, rgba(88,28,135,0.85) 0%, rgba(0,0,0,0) 100%);">
                  <span class="badge bg-white text-purple mb-2 rounded-pill px-3" style="color: #7e22ce;">Galería</span>
                  <h4 class="text-white fw-bold mb-0">{g0['title'][:60]}</h4>
                </div>
              </div>
            </a>
          </div>
          
          <!-- Columna Derecha: Grid 2x2 -->
          <div class="col-lg-6">
            <div class="row g-3 h-100">
              <div class="col-6">
                <a href="galeria.html#gallery-1" class="text-decoration-none">
                  <div class="position-relative overflow-hidden shadow-sm h-100" style="border-radius: 16px; min-height: 190px; cursor: pointer;">
                    <img src="{g1['images'][0] if g1['images'] else g1['cover']}" class="w-100 h-100" style="object-fit: cover; transition: transform 0.4s ease;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'" alt="{g1['title'][:50]}">
                    <div class="position-absolute bottom-0 start-0 w-100 p-3" style="background: linear-gradient(0deg, rgba(88,28,135,0.85) 0%, rgba(0,0,0,0) 100%);">
                      <h6 class="text-white fw-bold mb-0" style="font-size: 0.85rem;">{g1['title'][:45]}</h6>
                    </div>
                  </div>
                </a>
              </div>
              <div class="col-6">
                <a href="galeria.html#gallery-2" class="text-decoration-none">
                  <div class="position-relative overflow-hidden shadow-sm h-100" style="border-radius: 16px; min-height: 190px; cursor: pointer;">
                    <img src="{g2['images'][0] if g2['images'] else g2['cover']}" class="w-100 h-100" style="object-fit: cover; transition: transform 0.4s ease;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'" alt="{g2['title'][:50]}">
                    <div class="position-absolute bottom-0 start-0 w-100 p-3" style="background: linear-gradient(0deg, rgba(88,28,135,0.85) 0%, rgba(0,0,0,0) 100%);">
                      <h6 class="text-white fw-bold mb-0" style="font-size: 0.85rem;">{g2['title'][:45]}</h6>
                    </div>
                  </div>
                </a>
              </div>
              <div class="col-6">
                <a href="galeria.html#gallery-3" class="text-decoration-none">
                  <div class="position-relative overflow-hidden shadow-sm h-100" style="border-radius: 16px; min-height: 190px; cursor: pointer;">
                    <img src="{g3['images'][0] if g3['images'] else g3['cover']}" class="w-100 h-100" style="object-fit: cover; transition: transform 0.4s ease;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'" alt="{g3['title'][:50]}">
                    <div class="position-absolute bottom-0 start-0 w-100 p-3" style="background: linear-gradient(0deg, rgba(88,28,135,0.85) 0%, rgba(0,0,0,0) 100%);">
                      <h6 class="text-white fw-bold mb-0" style="font-size: 0.85rem;">{g3['title'][:45]}</h6>
                    </div>
                  </div>
                </a>
              </div>
              <div class="col-6">
                <a href="galeria.html#gallery-4" class="text-decoration-none">
                  <div class="position-relative overflow-hidden shadow-sm h-100" style="border-radius: 16px; min-height: 190px; cursor: pointer;">
                    <img src="{g4['images'][0] if g4['images'] else g4['cover']}" class="w-100 h-100" style="object-fit: cover; transition: transform 0.4s ease;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'" alt="{g4['title'][:50]}">
                    <div class="position-absolute bottom-0 start-0 w-100 p-3" style="background: linear-gradient(0deg, rgba(88,28,135,0.85) 0%, rgba(0,0,0,0) 100%);">
                      <h6 class="text-white fw-bold mb-0" style="font-size: 0.85rem;">{g4['title'][:45]}</h6>
                    </div>
                  </div>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>'''

# Replace the entire gallery section
pattern = r'<!-- SECCION GALERIA DESTACADA -->.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>'
# More precise: find from <!-- SECCION GALERIA DESTACADA --> to next unified-container closing
start_marker = '<!-- SECCION GALERIA DESTACADA -->'
start_idx = text.find(start_marker)
if start_idx == -1:
    print("ERROR: Could not find GALERIA section marker!")
else:
    # Find the closing </div> pattern that matches this section
    # Section structure: <div unified-container> ... </div> 
    # We need to find the matching end
    depth = 0
    i = start_idx
    found_first_div = False
    end_idx = -1
    while i < len(text):
        if text[i:i+4] == '<div':
            depth += 1
            found_first_div = True
        elif text[i:i+6] == '</div>':
            depth -= 1
            if found_first_div and depth == 0:
                end_idx = i + 6
                break
        i += 1
    
    if end_idx != -1:
        new_text = text[:start_idx] + new_gallery + text[end_idx:]
        
        # PART 3: Update menu links to point to galeria.html
        new_text = new_text.replace('href="/recursos/galeria"', 'href="galeria.html"')
        new_text = new_text.replace("href='recursos/galeria'", "href='galeria.html'")
        new_text = new_text.replace('href="recursos/galeria"', 'href="galeria.html"')
        
        with open('../index.html', 'w', encoding='utf-8') as f:
            f.write(new_text)
        print("Updated index.html gallery section with real data!")
        print("Updated menu links to galeria.html!")
    else:
        print("ERROR: Could not find end of gallery section!")

# PART 4: Also update the eventos.html menu link
with open('../pages/eventos.html', 'r', encoding='utf-8') as f:
    ev_text = f.read()
ev_text = ev_text.replace('href="/recursos/galeria"', 'href="galeria.html"')
with open('../pages/eventos.html', 'w', encoding='utf-8') as f:
    f.write(ev_text)
print("Updated eventos.html menu link!")

# PART 5: Update other HTML files menu links
import glob
for html_file in glob.glob('../pages/*.html'):
    if html_file in ['galeria.html', 'index.html', 'eventos.html']:
        continue
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if '/recursos/galeria' in content:
            content = content.replace('href="/recursos/galeria"', 'href="galeria.html"')
            content = content.replace("href='recursos/galeria'", "href='galeria.html'")
            content = content.replace('href="recursos/galeria"', 'href="galeria.html"')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated menu link in {html_file}")
    except Exception as e:
        print(f"Error updating {html_file}: {e}")

print("\n✅ ALL DONE!")
print("  - Created galeria.html with 5 galleries and lightbox viewer")
print("  - Updated home gallery section with real images and gradient overlays")
print("  - Updated all menu links to point to galeria.html")
