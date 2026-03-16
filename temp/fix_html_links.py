"""
Update HTML links to reflect new folder structure.
Pages moved from root to pages/ subfolder.
"""
import os
import glob

root = os.path.dirname(os.path.abspath(__file__))

# Pages that moved from root to pages/
page_files = [
    'biblioteca-virtual.html', 'boletines.html', 'campus-virtual.html',
    'educacion-tecnica.html', 'eventos.html', 'galeria.html',
    'innovatec.html', 'learn-english.html', 'noticias.html',
    'oferta-academica.html', 'plataforma-5.html', 'plataforma-6.html',
    'tec-creativa.html', 'videos.html'
]

quotes = ['"', "'"]

# =======================================================
# 1. Update index.html: page.html -> pages/page.html
# =======================================================
index_path = os.path.join(root, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

count = 0
for page in page_files:
    for q in quotes:
        old = 'href=' + q + page + q
        new = 'href=' + q + 'pages/' + page + q
        c = content.count(old)
        if c > 0:
            content = content.replace(old, new)
            count += c
        
        # Also onclick location.href
        old2 = "location.href='" + page + "'"
        new2 = "location.href='pages/" + page + "'"
        c2 = content.count(old2)
        if c2 > 0:
            content = content.replace(old2, new2)
            count += c2

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('index.html: ' + str(count) + ' links updated')

# =======================================================
# 2. Update centros/*.html and carreras/*.html
#    ../page.html -> ../pages/page.html
# =======================================================
count2 = 0
for pat in [os.path.join(root, 'centros', '*.html'), os.path.join(root, 'carreras', '*.html')]:
    for fpath in glob.glob(pat):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        changed = False
        for page in page_files:
            for q in quotes:
                old = 'href=' + q + '../' + page + q
                new = 'href=' + q + '../pages/' + page + q
                if old in content:
                    content = content.replace(old, new)
                    changed = True
                    count2 += content.count(new)  # approximate
        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

print('centros/ + carreras/: ' + str(count2) + ' links updated')

# =======================================================
# 3. Update noticias/*.html
# =======================================================
count3 = 0
for fpath in glob.glob(os.path.join(root, 'noticias', '*.html')):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    changed = False
    for page in page_files:
        for q in quotes:
            # From noticias/ -> ../page.html needs to be ../pages/page.html
            old = 'href=' + q + '../' + page + q
            new = 'href=' + q + '../pages/' + page + q
            if old in content:
                content = content.replace(old, new)
                changed = True
                count3 += 1
            # Direct references (shouldn't exist but just in case)
            old2 = 'href=' + q + page + q
            new2 = 'href=' + q + '../pages/' + page + q
            if old2 in content:
                content = content.replace(old2, new2)
                changed = True
                count3 += 1
    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

print('noticias/: ' + str(count3) + ' links updated')

# =======================================================
# 4. Update pages/*.html (cross-refs within pages folder)
# =======================================================
count4 = 0
for fpath in glob.glob(os.path.join(root, 'pages', '*.html')):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    changed = False
    
    # index.html is at ../index.html from pages/
    for q in quotes:
        old = 'href=' + q + 'index.html' + q
        new = 'href=' + q + '../index.html' + q
        if old in content:
            content = content.replace(old, new)
            changed = True
            count4 += 1
    
    # centros/ -> ../centros/ from pages/
    for q in quotes:
        old = 'href=' + q + 'centros/'
        new = 'href=' + q + '../centros/'
        if old in content:
            content = content.replace(old, new)
            changed = True
            count4 += 1
    
    # carreras/ -> ../carreras/ from pages/
    for q in quotes:
        old = 'href=' + q + 'carreras/'
        new = 'href=' + q + '../carreras/'
        if old in content:
            content = content.replace(old, new)
            changed = True
            count4 += 1
    
    # static/ -> ../static/ from pages/
    for prefix in ['src', 'href']:
        for q in quotes:
            old = prefix + '=' + q + 'static/'
            new = prefix + '=' + q + '../static/'
            if old in content:
                content = content.replace(old, new)
                changed = True
                count4 += 1
    
    # noticias/ -> ../noticias/ from pages/
    for q in quotes:
        old = 'href=' + q + 'noticias/'
        new = 'href=' + q + '../noticias/'
        if old in content:
            content = content.replace(old, new)
            changed = True
            count4 += 1
    
    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

print('pages/: ' + str(count4) + ' refs updated')
print('ALL HTML LINKS UPDATED!')
