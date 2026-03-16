import os
import glob
import re
import urllib.request

# Directorio de salida
out_dir = os.path.join(os.getcwd(), 'iconos_bootstrap_svg')
os.makedirs(out_dir, exist_ok=True)

# Buscar en todos los archivos HTML y JS del proyecto
files = glob.glob('../**/*.html', recursive=True) + glob.glob('../**/*.js', recursive=True)

icon_names = set()
for f in files:
    if 'node_modules' in f or '.git' in f:
        continue
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            # Buscar cualquier mención a "bi-[nombre]"
            matches = re.findall(r'\bbi-([a-z0-9\-]+)\b', content)
            for m in matches:
                icon_names.add(m)
    except Exception as e:
        pass

print(f"Se encontraron {len(icon_names)} posibles íconos de Bootstrap. Intentando descargarlos...")

descargados = 0
for icon in sorted(icon_names):
    url = f"https://raw.githubusercontent.com/twbs/icons/main/icons/{icon}.svg"
    out_path = os.path.join(out_dir, f"{icon}.svg")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            svg_content = resp.read()
            with open(out_path, 'wb') as f_out:
                f_out.write(svg_content)
            descargados += 1
            print(f"[{descargados}] Extraído y convertido a SVG: {icon}.svg")
    except Exception as e:
        # Algunos pueden no ser iconos oficiales o dar 404
        pass

print(f"\n¡Listo! {descargados} íconos SVG han sido descargados en la carpeta: {out_dir}")
