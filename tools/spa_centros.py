import os
import re

directory = r'd:\Respaldo José Rugama\Escritorio\Tecnologico Nacional 2026\centros'

script_to_add = """
  <!-- MICROSITE JS HANDLER -->
  <script>
    document.addEventListener("DOMContentLoaded", function() {
      const navLinks = document.querySelectorAll("#modernNavbarContent .nav-link");
      const tabs = document.querySelectorAll(".microsite-tab");
      
      navLinks.forEach(link => {
        link.addEventListener("click", function(e) {
          const href = this.getAttribute("href");
          if (href && href.startsWith("#")) {
            e.preventDefault();
            const targetId = "tab-" + href.substring(1); 
            
            if (document.getElementById(targetId)) {
              tabs.forEach(tab => { tab.style.display = "none"; });
              navLinks.forEach(nav => nav.classList.remove("active"));
              
              document.getElementById(targetId).style.display = "block";
              this.classList.add("active");
              
              const inicioBanner = document.getElementById("inicio");
              if (inicioBanner) {
                 window.scrollTo({
                    top: inicioBanner.offsetTop - 30, // scroll to slightly below top of banner to see padding
                    behavior: "smooth"
                 });
              }
            }
          }
        });
      });
    });
  </script>
</body>
"""

files_changed = 0

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        breadcrumb_match = re.search(r'<!-- Breadcrumb -->\s*<nav aria-label="breadcrumb".*?</nav>', content, re.DOTALL)
        acerca_match = re.search(r'<!-- Center Header -->\s*(<div id="acerca"[\s\S]*?)<!-- Careers Section -->', content)
        carreras_match = re.search(r'<!-- Careers Section -->\s*(<div id="carreras"[\s\S]*?)<!-- Quick Info -->', content)
        cursos_match = re.search(r'<!-- Quick Info -->\s*(<div id="cursos"[\s\S]*?)</div>\s*<footer>', content)

        if breadcrumb_match and acerca_match and carreras_match and cursos_match:
            breadcrumb = breadcrumb_match.group(0)
            acerca = acerca_match.group(1).strip()
            carreras = carreras_match.group(1).strip()
            cursos_info = cursos_match.group(1).strip()
            
            new_container = f'''  <div class="container py-5 microsite-container" style="min-height: 500px;">
    {breadcrumb}

    <!-- TAB: INICIO -->
    <div id="tab-inicio" class="microsite-tab">
      <!-- Center Header -->
      {acerca}
      
      <!-- Current courses/info placeholders -->
      {cursos_info}
      
      <!-- Careers Section -->
      {carreras}
    </div>

    <!-- TAB: ACERCA DE -->
    <div id="tab-acerca" class="microsite-tab" style="display:none;">
      {acerca}
    </div>

    <!-- TAB: CARRERAS -->
    <div id="tab-carreras" class="microsite-tab" style="display:none;">
      {carreras}
    </div>

    <!-- TAB: CURSOS -->
    <div id="tab-cursos" class="microsite-tab" style="display:none;">
      <h4 class="fw-bold mb-4" style="color:#1e293b;">
        <i class="bi-journal-bookmark-fill text-primary me-2"></i>Cursos Libres y Modulares
      </h4>
      {cursos_info}
      <div class="alert alert-info border-0 shadow-sm mt-4" style="border-radius:12px;">En este momento estamos actualizando nuestra oferta detallada de cursos de capacitación.</div>
    </div>

    <!-- TAB: NOTICIAS -->
    <div id="tab-noticias" class="microsite-tab" style="display:none;">
      <h4 class="fw-bold mb-4" style="color:#1e293b;">
        <i class="bi-newspaper text-primary me-2"></i>Últimas Noticias
      </h4>
      <div class="alert alert-info border-0 shadow-sm" style="border-radius:12px;">Próximamente publicaremos recortes, comunicados y notas de prensa de nuestras actividades.</div>
    </div>

    <!-- TAB: GALERÍA -->
    <div id="tab-galeria" class="microsite-tab" style="display:none;">
      <h4 class="fw-bold mb-4" style="color:#1e293b;">
        <i class="bi-images text-primary me-2"></i>Galería Fotográfica
      </h4>
      <div class="alert alert-info border-0 shadow-sm" style="border-radius:12px;">Nuestra galería de recorridos fotográficos está en construcción.</div>
    </div>
  </div>
'''
            
            # Replace old container and its contents up to <footer>
            content = re.sub(
                r'<div class="container py-5">[\s\S]*?</div>\s*<footer>',
                new_container + '\n<footer>',
                content
            )
            
            # Inject script if not present
            if 'MICROSITE JS HANDLER' not in content:
                content = content.replace('</body>', script_to_add)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            files_changed += 1

print(f'Done! Upgraded to SPA in {files_changed} files.')
