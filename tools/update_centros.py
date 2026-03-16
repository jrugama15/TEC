import os
import re

directory = r'd:\Respaldo José Rugama\Escritorio\Tecnologico Nacional 2026\centros'

menu_replacement = """        <ul class="navbar-nav ms-auto mb-0 align-items-lg-center">
          <li class="nav-item"><a class="nav-link active" aria-current="page" href="#inicio">INICIO</a></li>
          <li class="nav-item"><a class="nav-link" href="#acerca">ACERCA DE</a></li>
          <li class="nav-item"><a class="nav-link" href="#carreras">CARRERAS</a></li>
          <li class="nav-item"><a class="nav-link" href="#cursos">CURSOS</a></li>
          <li class="nav-item"><a class="nav-link" href="#noticias">NOTICIAS</a></li>
          <li class="nav-item"><a class="nav-link" href="#galeria">GALERÍA</a></li>
        </ul>"""

files_changed = 0

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        
        # Replace the Navbar UL
        new_content = re.sub(
            r'<ul class=\"navbar-nav ms-auto mb-0 align-items-lg-center\">.*?</ul>',
            menu_replacement,
            new_content,
            flags=re.DOTALL
        )
        
        # Add id='inicio' to subpage-banner if not present
        if 'id="inicio"' not in new_content:
            new_content = new_content.replace(
                '<section class="subpage-banner"',
                '<section id="inicio" class="subpage-banner"'
            )
            
        # Add id='acerca' to the Center Header
        if 'id="acerca"' not in new_content:
            new_content = new_content.replace(
                '<!-- Center Header -->\n    <div class="row mb-5">',
                '<!-- Center Header -->\n    <div id="acerca" class="row mb-5 pt-5">'
            )
            
        # Add id='carreras' to Careers section
        if '<!-- Careers Section -->' in new_content and 'id="carreras"' not in new_content:
            new_content = new_content.replace(
                '<!-- Careers Section -->\n    <div class="mb-5">',
                '<!-- Careers Section -->\n    <div id="carreras" class="mb-5 pt-5">'
            )
            
        # Quick Info might be 'cursos' temporarily, to have anchors match
        if '<!-- Quick Info -->' in new_content and 'id="cursos"' not in new_content:
            new_content = new_content.replace(
                '<!-- Quick Info -->\n    <div class="row g-4 mb-5">',
                '<!-- Quick Info -->\n    <div id="cursos" class="row g-4 mb-5 pt-5">'
            )
        
        # Find the title to use in the banner overlay
        match = re.search(r'<h2 class="fw-bold mb-3" style="color:#1e293b;">(.*?)</h2>', new_content)
        title = match.group(1) if match else ''

        # Apply overlay text to banner if not present
        if '<div class="banner-overlay"' not in new_content and 'subpage-banner' in new_content:
            def replacer(m):
                img_tag = m.group(1)
                img_tag = img_tag.replace('max-height: 380px;', 'height: 100%;') # fix img height for overlay
                overlay = f"""
    <div class="banner-overlay" style="position: absolute; top:0; left:0; width:100%; height:100%; background:rgba(10, 61, 107, 0.4); display:flex; align-items:center; justify-content:center;">
        <h1 class="text-white fw-bold text-center px-3" style="font-size: 2.5rem; text-shadow: 2px 2px 6px rgba(0,0,0,0.6);">{title}</h1>
    </div>
  </section>"""
                return f'<section id="inicio" class="subpage-banner" style="margin-top: 55px; width: 100%; position: relative; height:380px; overflow:hidden;">\n    {img_tag}{overlay}'

            new_content = re.sub(
                r'<section [^>]*class="subpage-banner"[^>]*>\s*(<img[^>]+>)\s*</section>',
                replacer,
                new_content
            )

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_changed += 1

print(f'Done! Changed {files_changed} files.')
