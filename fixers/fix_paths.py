import os
import glob

# Fix relative paths in subfolders - they need ../ prefix
count = 0
for pattern in ['../centros/*.html', '../carreras/*.html']:
    for f in glob.glob(pattern):
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        # Fix static paths
        content = content.replace('src="static/', 'src="../static/')
        content = content.replace('href="static/', 'href="../static/')
        
        # Fix page links
        content = content.replace('href="index.html"', 'href="../index.html"')
        content = content.replace('href="oferta-academica.html"', 'href="../oferta-academica.html"')
        content = content.replace('href="carreras-educacion-tecnica.html"', 'href="../carreras-educacion-tecnica.html"')
        content = content.replace('href="noticias.html"', 'href="../noticias.html"')
        content = content.replace('href="eventos.html"', 'href="../eventos.html"')
        content = content.replace('href="videos.html"', 'href="../videos.html"')
        content = content.replace('href="galeria.html"', 'href="../galeria.html"')
        content = content.replace('href="boletines.html"', 'href="../boletines.html"')
        content = content.replace('href="biblioteca-virtual.html"', 'href="../biblioteca-virtual.html"')
        
        # Fix career links from center pages
        content = content.replace('href="carreras/', 'href="../carreras/')
        
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content)
        count += 1

print(f"Fixed relative paths in {count} files")
