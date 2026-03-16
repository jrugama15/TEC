import os, glob

centros = len(os.listdir('../centros'))
carreras = len(os.listdir('../carreras'))
print(f'centros/: {centros} files')
print(f'carreras/: {carreras} files')
print(f'carreras-educacion-tecnica.html exists: {os.path.exists("../pages/carreras-educacion-tecnica.html")}')

with open('../centros/centro-tecnologico-alcides-miranda-fitoria.html','r',encoding='utf-8') as f:
    t = f.read()
print(f'Center page size: {len(t)} bytes')
print('Has ../static:', '../static' in t)
print('Has ../index.html:', '../index.html' in t)
print('Has correct banner:', 'sueño' in t)

career_files = glob.glob('../carreras/*.html')
if career_files:
    with open(career_files[0],'r',encoding='utf-8') as f:
        t = f.read()
    print(f'Career page: {career_files[0]} - {len(t)} bytes')
    print('Has ../static:', '../static' in t)
