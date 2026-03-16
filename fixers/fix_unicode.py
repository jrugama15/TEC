import os
import glob

# Fix unicode escapes in generated HTML files
bad = 'Construyo_mi_sue\\u00f1o_en_el_Tecnol\\u00f3gico_Nacional.jpeg'
good = 'Construyo_mi_sueño_en_el_Tecnológico_Nacional.jpeg'

count = 0
for pattern in ['../centros/*.html', '../carreras/*.html', '../pages/carreras-educacion-tecnica.html']:
    for f in glob.glob(pattern):
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        if bad in content:
            content = content.replace(bad, good)
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(content)
            count += 1

print(f"Fixed unicode escapes in {count} files")
