"""
Script maestro para actualizar todas las rutas en los scripts Python
después de la reorganización del proyecto.

Los scripts se movieron a subcarpetas (builders/, tools/, fixers/)
y necesitan usar rutas relativas con ../ para acceder a archivos
en la raíz del proyecto o en otras subcarpetas.
"""
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# ===================================================================
# Define all path replacements per folder
# Format: (folder, filename, [(old_string, new_string), ...])
# ===================================================================

replacements = []

# ===================== BUILDERS =====================

# build_all_pages.py - reads JSON data, reads/writes HTML, creates centros/ and carreras/
replacements.append(('builders', 'build_all_pages.py', [
    ("open('centers.json'",           "open('../data/centers.json'"),
    ("open('careers.json'",           "open('../data/careers.json'"),
    ("open('eventos.html'",           "open('../pages/eventos.html'"),
    ("os.makedirs('centros'",         "os.makedirs('../centros'"),
    ("os.makedirs('carreras'",        "os.makedirs('../carreras'"),
    ("f'centros/{slug}.html'",        "f'../centros/{slug}.html'"),
    ("f'carreras/{slug}.html'",       "f'../carreras/{slug}.html'"),
    ("open('educacion-tecnica.html', 'w'", "open('../pages/educacion-tecnica.html', 'w'"),
    ("open('index.html', 'r'",        "open('../index.html', 'r'"),
    ("open('index.html', 'w'",        "open('../index.html', 'w'"),
]))

# build_educacion_tecnica.py - reads careers.json, reads eventos.html, writes educacion-tecnica.html
replacements.append(('builders', 'build_educacion_tecnica.py', [
    ("open('careers.json'",           "open('../data/careers.json'"),
    ("open('eventos.html'",           "open('../pages/eventos.html'"),
    ("open('educacion-tecnica.html', 'w'", "open('../pages/educacion-tecnica.html', 'w'"),
]))

# build_gallery.py - reads galleries.json, writes galeria.html, reads/writes index.html, reads/writes eventos.html, reads/writes *.html
replacements.append(('builders', 'build_gallery.py', [
    ("open('galleries.json'",         "open('../data/galleries.json'"),
    ("open('galeria.html', 'w'",      "open('../pages/galeria.html', 'w'"),
    ("open('index.html', 'r'",        "open('../index.html', 'r'"),
    ("open('index.html', 'w'",        "open('../index.html', 'w'"),
    ("open('eventos.html', 'r'",      "open('../pages/eventos.html', 'r'"),
    ("open('eventos.html', 'w'",      "open('../pages/eventos.html', 'w'"),
    ("glob.glob('*.html')",           "glob.glob('../pages/*.html')"),
]))

# inject_slider.py - reads events.json, reads/writes index.html
replacements.append(('builders', 'inject_slider.py', [
    ("open('events.json'",            "open('../data/events.json'"),
    ("open('index.html', 'r'",        "open('../index.html', 'r'"),
    ("open('index.html', 'w'",        "open('../index.html', 'w'"),
]))

# update_center_links.py - reads centers.json, reads/writes index.html
replacements.append(('builders', 'update_center_links.py', [
    ("open('centers.json'",           "open('../data/centers.json'"),
    ("open('index.html', 'r'",        "open('../index.html', 'r'"),
    ("open('index.html', 'w'",        "open('../index.html', 'w'"),
]))

# update_events_html.py - reads events.json, reads/writes eventos.html
replacements.append(('builders', 'update_events_html.py', [
    ("open('events.json'",            "open('../data/events.json'"),
    ("open('eventos.html', 'r'",      "open('../pages/eventos.html', 'r'"),
    ("open('eventos.html', 'w'",      "open('../pages/eventos.html', 'w'"),
]))

# update_events_page.py - reads events.json, reads/writes eventos.html
replacements.append(('builders', 'update_events_page.py', [
    ("open('events.json'",            "open('../data/events.json'"),
    ("open('eventos.html', 'r'",      "open('../pages/eventos.html', 'r'"),
    ("open('eventos.html', 'w'",      "open('../pages/eventos.html', 'w'"),
]))

# ===================== TOOLS =====================

# scrape_all_careers.py - writes careers.json
replacements.append(('tools', 'scrape_all_careers.py', [
    ("open('careers.json', 'w'",      "open('../data/careers.json', 'w'"),
]))

# scrape_all_centers.py - writes centers.json
replacements.append(('tools', 'scrape_all_centers.py', [
    ("open('centers.json', 'w'",      "open('../data/centers.json', 'w'"),
]))

# scrape_center_careers.py - reads/writes centers.json
replacements.append(('tools', 'scrape_center_careers.py', [
    ("open('centers.json', 'r'",      "open('../data/centers.json', 'r'"),
    ("open('centers.json', 'w'",      "open('../data/centers.json', 'w'"),
]))

# extract_events.py - reads eventos_scraped.html, writes events.json
replacements.append(('tools', 'extract_events.py', [
    ('open("eventos_scraped.html"',   'open("../temp/eventos_scraped.html"'),
    ('open("events.json"',            'open("../data/events.json"'),
]))

# check_careers.py - reads careers.json
replacements.append(('tools', 'check_careers.py', [
    ("open('careers.json'",           "open('../data/careers.json'"),
]))

# scrape_galleries_full.py - writes galleries.json
replacements.append(('tools', 'scrape_galleries_full.py', [
    ("open('galleries.json', 'w'",    "open('../data/galleries.json', 'w'"),
]))

# scrape_docs.py - reads/writes index.html
replacements.append(('tools', 'scrape_docs.py', [
    ("open('index.html', 'r'",        "open('../index.html', 'r'"),
    ("open('index.html', 'w'",        "open('../index.html', 'w'"),
]))

# ===================== FIXERS =====================

# add_footer_galeria.py - reads eventos.html, reads/writes galeria.html
replacements.append(('fixers', 'add_footer_galeria.py', [
    ("open('eventos.html'",           "open('../pages/eventos.html'"),
    ("open('galeria.html', 'r'",      "open('../pages/galeria.html', 'r'"),
    ("open('galeria.html', 'w'",      "open('../pages/galeria.html', 'w'"),
]))

# apply_real_docs.py - reads/writes index.html
replacements.append(('fixers', 'apply_real_docs.py', [
    ("open('index.html', 'r'",        "open('../index.html', 'r'"),
    ("open('index.html', 'w'",        "open('../index.html', 'w'"),
]))

# apply_real_docs2.py - reads/writes index.html
replacements.append(('fixers', 'apply_real_docs2.py', [
    ("open('index.html', 'r'",        "open('../index.html', 'r'"),
    ("open('index.html', 'w'",        "open('../index.html', 'w'"),
]))

# apply_real_docs3.py - reads/writes index.html
replacements.append(('fixers', 'apply_real_docs3.py', [
    ("open('index.html', 'r'",        "open('../index.html', 'r'"),
    ("open('index.html', 'w'",        "open('../index.html', 'w'"),
]))

# apply_real_docs_final.py - reads/writes index.html
replacements.append(('fixers', 'apply_real_docs_final.py', [
    ("open('index.html', 'r'",        "open('../index.html', 'r'"),
    ("open('index.html', 'w'",        "open('../index.html', 'w'"),
]))

# fix_paths.py - reads/writes centros/*.html, carreras/*.html
replacements.append(('fixers', 'fix_paths.py', [
    ("['centros/*.html', 'carreras/*.html']", "['../centros/*.html', '../carreras/*.html']"),
]))

# fix_unicode.py - reads/writes centros/*.html, carreras/*.html, educacion-tecnica.html
replacements.append(('fixers', 'fix_unicode.py', [
    ("['centros/*.html', 'carreras/*.html', 'educacion-tecnica.html']", 
     "['../centros/*.html', '../carreras/*.html', '../pages/educacion-tecnica.html']"),
]))

# verify_all.py - reads centros/, carreras/
replacements.append(('fixers', 'verify_all.py', [
    ("os.listdir('centros')",                 "os.listdir('../centros')"),
    ("os.listdir('carreras')",                "os.listdir('../carreras')"),
    ('os.path.exists("educacion-tecnica.html")', 'os.path.exists("../pages/educacion-tecnica.html")'),
    ("open('centros/centro-tecnologico-alcides-miranda-fitoria.html'", 
     "open('../centros/centro-tecnologico-alcides-miranda-fitoria.html'"),
    ("glob.glob('carreras/*.html')",          "glob.glob('../carreras/*.html')"),
]))

# verify_grid.py - reads eventos.html
replacements.append(('fixers', 'verify_grid.py', [
    ("open('eventos.html'",                   "open('../pages/eventos.html'"),
]))

# inspect_3.py - reads eventos_scraped.html
replacements.append(('fixers', 'inspect_3.py', [
    ('open("eventos_scraped.html"',           'open("../temp/eventos_scraped.html"'),
]))

# inspect_events.py - reads eventos_scraped.html
replacements.append(('fixers', 'inspect_events.py', [
    ('open("eventos_scraped.html"',           'open("../temp/eventos_scraped.html"'),
]))

# inspect_events2.py - reads eventos_scraped.html
replacements.append(('fixers', 'inspect_events2.py', [
    ('open("eventos_scraped.html"',           'open("../temp/eventos_scraped.html"'),
]))

# ===================================================================
# Apply all replacements
# ===================================================================

total_changes = 0
total_files = 0

for folder, filename, subs in replacements:
    filepath = os.path.join(PROJECT_ROOT, folder, filename)
    if not os.path.exists(filepath):
        print(f"  [!] NOT FOUND: {folder}/{filename}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    file_changes = 0
    
    for old, new in subs:
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            file_changes += count
    
    if file_changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        total_changes += file_changes
        total_files += 1
        print(f"  [OK] {folder}/{filename}: {file_changes} rutas actualizadas")
    else:
        print(f"  [--] {folder}/{filename}: sin cambios necesarios")

# ===================================================================
# Also check PowerShell scripts in scripts/
# ===================================================================
print("\n=== Verificando scripts PowerShell ===")
for ps_file in ['add_comments.ps1', 'fix_navbar.ps1', 'optimize.ps1']:
    filepath = os.path.join(PROJECT_ROOT, 'scripts', ps_file)
    if not os.path.exists(filepath):
        print(f"  [!] NOT FOUND: scripts/{ps_file}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # These use absolute paths, so they should be fine
    if 'index.html' in content and 'Tecnologico Nacional 2026\\index.html' in content:
        print(f"  [OK] scripts/{ps_file}: usa rutas absolutas, no requiere cambio")
    else:
        print(f"  [i] scripts/{ps_file}: revisar manualmente")

print(f"\n{'='*50}")
print(f"COMPLETADO: {total_changes} rutas actualizadas en {total_files} archivos")
print(f"{'='*50}")
