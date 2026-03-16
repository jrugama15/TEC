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
        
        # We need to replace everything from <div id="modernNavbarContent"> to its closing </div>
        # before the final container </div>.
        
        new_content = re.sub(
            r'<div class="collapse navbar-collapse" id="modernNavbarContent">.*?</div>\s+</div>\s+</nav>',
            f'<div class="collapse navbar-collapse" id="modernNavbarContent">\n{menu_replacement}\n      </div>\n    </div>\n  </nav>',
            content,
            flags=re.DOTALL
        )

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_changed += 1

print(f'Done! Fixed navbar in {files_changed} files.')
