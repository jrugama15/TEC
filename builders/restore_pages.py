import urllib.request
import os
import re

print('Restaurando desde live site y local backups...')

urls_to_get = [
    ('http://websitemigrado.desarrollo.tecnacional.edu.ni/educacion-tecnica/carreras', '../pages/carreras-educacion-tecnica.html'),
    ('http://websitemigrado.desarrollo.tecnacional.edu.ni/educacion-tecnica', '../pages/oferta-academica.html'),
    ('http://websitemigrado.desarrollo.tecnacional.edu.ni/centros-tecnologicos', '../pages/centros-tecnologicos.html')
]

for url, path in urls_to_get:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            
            # Cambiar links de recursos en el HTML de live al local relativo
            content = content.replace('"/static/', '"../static/')
            content = content.replace("'/static/", "'../static/")
            content = content.replace('"/media/', '"../media/')
            content = content.replace("'/media/", "'../media/")
            content = content.replace('https://www.tecnacional.edu.ni/media/', '../media/')
            
            # Save
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Restaurado {path}')
    except Exception as e:
        print(f'Error descargando {url}: {e}')

# Sacar de build_all_pages la generacion que sobreescribe carreras-educacion-tecnica.html
with open('build_all_pages.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Borrar la parte que crea carreras-educacion-tecnica manualmente
if 'CREATE CARRERAS-EDUCACION-TECNICA.HTML WITH TABS' in text:
    part_to_remove = re.search(r'# =========================================================\n# CREATE CARRERAS-EDUCACION-TECNICA\.HTML WITH TABS\n# =========================================================[\s\S]*?print\(\"  Created carreras-educacion-tecnica\.html\"\)', text)
    if part_to_remove:
        text = text[:part_to_remove.start()] + text[part_to_remove.end():]
        with open('build_all_pages.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print('Se eliminó la sobrescritura en build_all_pages.py')

