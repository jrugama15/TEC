import glob

files = glob.glob('../pages/*.html')
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'href="/educacion-tecnica"' in c:
        c = c.replace('href="/educacion-tecnica"', 'href="carreras-educacion-tecnica.html"')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)

with open('../index.html', 'r', encoding='utf-8') as f:
    c = f.read()
if 'href="/educacion-tecnica"' in c:
    c = c.replace('href="/educacion-tecnica"', 'href="pages/carreras-educacion-tecnica.html"')
    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(c)

# We also need to fix build_all_pages.py to correctly set the path inside centros/ and carreras/
with open('build_all_pages.py', 'r', encoding='utf-8') as f:
    builder = f.read()

# I will replace the occurence in NAVBAR before loop injecting:
# In generate logic:
# wait, actually, build_all_pages.py reads from eventos.html.
# if I just fixed eventos.html to point to "carreras-educacion-tecnica.html", 
# then build_all_pages.py will inject href="carreras-educacion-tecnica.html", which is WRONG for centros/ and carreras/ because they need "../pages/..."
# In build_all_pages.py we had `FOOTER = re.sub(...)`.
# Instead of doing that, let's fix the NAVBAR before we inject it to the centros!
