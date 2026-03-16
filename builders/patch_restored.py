import glob
import re

files = ['../pages/carreras-educacion-tecnica.html', '../pages/oferta-academica.html', '../pages/centros-tecnologicos.html']
for f in files:
    with open(f, 'r', encoding='utf-8') as fr:
        c = fr.read()
    
    # Arreglos de rutas al ser descargados de internet
    c = c.replace('href="/educacion-tecnica/carreras"', 'href="carreras-educacion-tecnica.html"')
    c = c.replace('href="/educacion-tecnica"', 'href="oferta-academica.html"')
    c = c.replace('href="/centros-tecnologicos"', 'href="centros-tecnologicos.html"')
    c = c.replace('href="/empresas/"', 'href="empresas.html"')
    c = c.replace('href="/recursos/noticia"', 'href="noticias.html"')
    c = c.replace('href="/recursos/evento"', 'href="eventos.html"')
    c = c.replace('href="/recursos/video"', 'href="videos.html"')
    c = c.replace('href="/recursos/galeria"', 'href="galeria.html"')
    c = c.replace('href="/recursos/boletin"', 'href="boletines.html"')
    c = c.replace('href="/recursos/calidad"', 'href="calidad.html"')
    c = c.replace('href="/recursos/documento"', 'href="adquisiciones.html"')
    
    # Change absolute URLs if present
    c = c.replace('https://www.tecnacional.edu.ni/media/', '../media/')
    c = c.replace('href="/static/', 'href="../static/')
    c = c.replace('src="/static/', 'src="../static/')

    with open(f, 'w', encoding='utf-8') as fw:
        fw.write(c)

print('Páginas restauradas con los links locales listos.')
import update_social
