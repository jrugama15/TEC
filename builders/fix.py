import glob

files = glob.glob('../pages/*.html')
if '../index.html' not in files:
    files.append('../index.html')

replacements = [
    ('href="/educacion-tecnica/carreras"', 'href="oferta-academica.html"'),
    ('href="/centros-tecnologicos"', 'href="centros-tecnologicos.html"'),
    ('href="/empresas/"', 'href="empresas.html"'),
    ('href="/recursos/boletin"', 'href="boletines.html"'),
    ('href="/recursos/evento"', 'href="eventos.html"'),
    ('href="https://mapa.tecnacional.edu.ni/innovatec"', 'href="innovatec.html"'),
    ('href="/podcast/"', 'href="podcast.html"'),
    ('href="http://campus.inatec.edu.ni/"', 'href="campus-virtual.html"'),
    ('href="/programas"', 'href="programas.html"'),
    ('href="/experiencia-laboral"', 'href="experiencia-laboral.html"'),
    ('href="/recursos/calidad"', 'href="calidad.html"'),
    ('href="/recursos/documento"', 'href="adquisiciones.html"'),
    ('href="/congreso/"', 'href="congreso.html"')
]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    for old, new in replacements:
        if file.endswith('index.html'):
            new_idx = new.replace('href="', 'href="pages/')
            if old in content:
                content = content.replace(old, new_idx)
                modified = True
        else:
            if old in content:
                content = content.replace(old, new)
                modified = True

    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {file}')
