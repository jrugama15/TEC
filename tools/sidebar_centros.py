import os
import re

directory = r'd:\Respaldo José Rugama\Escritorio\Tecnologico Nacional 2026\centros'

sidebar_html = """    </div> <!-- Close col-lg-8 -->

    <!-- SIDEBAR WIDGETS -->
    <div class="col-lg-4 col-xl-4 mt-5 mt-lg-0">
      <!-- Buscador Widget -->
      <div class="p-4 rounded-3 mb-4 shadow-sm" style="background-color: #2ea3db; color: #ffffff;">
        <h5 class="fw-bold mb-3" style="font-family: inherit; font-size: 1.25rem;">Buscador de cursos y carreras</h5>
        <form>
          <div class="form-check mb-2">
            <input class="form-check-input" type="radio" name="searchType" id="searchCarreras" value="carreras" checked>
            <label class="form-check-label fw-semibold" for="searchCarreras" style="font-size: 0.9rem;">Carreras Técnicas</label>
          </div>
          <div class="form-check mb-3">
            <input class="form-check-input" type="radio" name="searchType" id="searchCursos" value="cursos">
            <label class="form-check-label fw-semibold" for="searchCursos" style="font-size: 0.9rem;">Cursos de Capacitación</label>
          </div>
          <div class="row g-2 mb-2">
            <div class="col-6">
              <select class="form-select form-select-sm border-0 rounded-1" style="color: #6c757d; font-size: 0.85rem; padding: 0.4rem;">
                <option value="">Sector</option>
              </select>
            </div>
            <div class="col-6">
              <select class="form-select form-select-sm border-0 rounded-1" style="color: #6c757d; font-size: 0.85rem; padding: 0.4rem;">
                <option value="">Rubro</option>
              </select>
            </div>
          </div>
          <div class="mb-3">
            <input type="text" class="form-control form-control-sm border-0 rounded-1" placeholder="Nombre de la carrera" style="font-size: 0.85rem; padding: 0.4rem;">
          </div>
          <div class="text-end mb-3">
            <button type="button" class="btn btn-sm text-white fw-bold px-3 py-1" style="background-color: #e91e63; border-radius: 3px;">Buscar</button>
          </div>
        </form>
        <div class="mb-3" style="font-size: 0.8rem;">
          <a href="#" class="text-white text-decoration-none fw-semibold d-block mb-1 hover-opacity">Mostrar todas las carreras</a>
          <a href="#" class="text-white text-decoration-none fw-semibold d-block hover-opacity">Mostrar todos los cursos</a>
        </div>
        <hr style="border-top: 1px solid rgba(255,255,255,0.7); opacity: 1; margin: 15px 0;">
        <h6 class="fw-bold mb-2" style="font-size:0.95rem;">Contactenos</h6>
        <div class="d-flex gap-2">
          <a href="https://www.facebook.com/TecNacional/" target="_blank" class="bg-white rounded-1 d-flex align-items-center justify-content-center shadow-sm" style="width: 32px; height: 32px; text-decoration: none; transition: transform 0.2s;">
            <i class="bi-facebook" style="color: #2ea3db; font-size: 1.1rem;"></i>
          </a>
          <a href="https://twitter.com/TecNacional" target="_blank" class="bg-white rounded-1 d-flex align-items-center justify-content-center shadow-sm" style="width: 32px; height: 32px; text-decoration: none; transition: transform 0.2s;">
            <i class="bi-twitter" style="color: #2ea3db; font-size: 1.1rem;"></i>
          </a>
          <a href="https://www.youtube.com/c/TecNacional" target="_blank" class="bg-white rounded-1 d-flex align-items-center justify-content-center shadow-sm" style="width: 32px; height: 32px; text-decoration: none; transition: transform 0.2s;">
            <i class="bi-youtube" style="color: #2ea3db; font-size: 1.1rem;"></i>
          </a>
        </div>
      </div>

      <!-- Noticias Widget -->
      <div class="rounded-3 overflow-hidden shadow-sm border border-secondary border-opacity-25 pb-3" style="background-color: #eef1f3;">
        <div class="p-3 text-white" style="background-color: #14578b;">
          <h5 class="fw-bold mb-0" style="font-family: inherit; font-size: 1.1rem; letter-spacing: 0.5px;">Noticias</h5>
        </div>
        <!-- Featured News -->
        <div class="bg-white">
          <img src="https://www.tecnacional.edu.ni/media/Mural_jcu.jpg" alt="Noticia" style="width:100%; height:140px; object-fit:cover;">
          <div class="p-3 border-bottom">
            <a href="#" class="text-decoration-none d-block mb-2" style="color: #1a72b0; font-size: 0.95rem; font-weight: 600; line-height: 1.3;">Un mural que cuenta historia e identidad: "Cumpliendo el Sueño de Sandino"</a>
            <p class="text-muted mb-0" style="font-size: 0.85rem; line-height: 1.4;">En un desborde de creatividad y compromiso revolucionario, el Tecnológico Nacional, a través del Centro Cultural y Politécnico José ...</p>
          </div>
        </div>
        <!-- Other News Links -->
        <div class="p-3">
          <a href="#" class="text-decoration-none d-block mb-3" style="color: #1a72b0; font-size: 0.9rem; line-height: 1.3;">Conversatorio "Educación Artística y Cultural: Pensar en Darío Hoy" Reúne a Expertos en Nicaragua</a>
          <a href="#" class="text-decoration-none d-block" style="color: #1a72b0; font-size: 0.9rem; line-height: 1.3;">Cuando la poesía canta a la patria: lanzamiento del concurso Canto Azul y Patria</a>
        </div>
      </div>
    </div>
  </div> <!-- Close outer row -->
"""

files_changed = 0
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if '<div class="row microsite-layout">' not in content:
            # 1. Start the row / col layout
            new_content = re.sub(
                r'(<nav aria-label="breadcrumb".*?</nav>)\s*<!-- TAB: INICIO -->',
                r'\1\n\n  <div class="row microsite-layout">\n    <div class="col-lg-8 col-xl-8">\n      <!-- TAB: INICIO -->',
                content,
                flags=re.DOTALL
            )
            
            # 2. Insert the sidebar and close it right before <footer>
            new_content = re.sub(
                r'    </div>\s*</div>\s*<footer>',
                sidebar_html + '\n</div>\n\n<footer>',
                new_content
            )
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                files_changed += 1

print(f"Done! Changed: {files_changed}")
