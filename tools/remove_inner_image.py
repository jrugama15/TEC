import os
import re

directory = r'd:\Respaldo José Rugama\Escritorio\Tecnologico Nacional 2026\centros'

files_changed = 0

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        
        # 1. Quitar el contenedor de la imagen en <div class="col-lg-6 mt-4 mt-lg-0">...</div>
        # Vamos a ser un poco más flexibles con el interior por si varían los links/alts
        new_content = re.sub(
            r'<div class="col-lg-6 mt-4 mt-lg-0">\s*<div class="rounded-4 overflow-hidden shadow-sm" style="height:300px;">\s*<img[^>]+>\s*</div>\s*</div>',
            '',
            new_content
        )
        
        # 2. Como quitamos la mitad de la columna (col-lg-6), es mejor expandir la descripción
        # para que ocupe todo el ancho disponible (col-lg-12).
        new_content = re.sub(
            r'(<div id="acerca" class="row mb-5 pt-5">\s*)<div class="col-lg-6">',
            r'\1<div class="col-lg-12">',
            new_content
        )
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_changed += 1

print(f"Removed image container and expanded text area in {files_changed} files.")
