import os
import re

directory = r'd:\Respaldo José Rugama\Escritorio\Tecnologico Nacional 2026\centros'

files_changed = 0

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        
        # 1. Fix the missing tag closing issue around `tab-galeria` inside `col-lg-8`
        # Current broken layout: 
        # <div class="alert alert-info border-0 shadow-sm" style="border-radius:12px;">Nuestra galería de recorridos fotográficos está en construcción.</div>
        #     </div> <!-- Close col-lg-8 -->
        # We need to turn that single </div> into TWO </div>s: one for tab-galeria, and one for col-lg-8
        
        new_content = re.sub(
            r'Nuestra galería de recorridos fotográficos está en construcción\.</div>\s*</div> <!-- Close col-lg-8 -->',
            'Nuestra galería de recorridos fotográficos está en construcción.</div>\n    </div> <!-- Close tab-galeria -->\n    </div> <!-- Close col-lg-8 -->',
            new_content
        )
        
        # 2. Fix the thumbnail image path (Mural_jcu.jpg -> correct INATEC url)
        new_content = new_content.replace(
            '<img src="https://www.tecnacional.edu.ni/media/Mural_jcu.jpg"',
            '<img src="https://www.tecnacional.edu.ni/media/Un_mural_que_cuenta_historia_e_identidad_Cumpliendo_el_Sue%C3%B1o_de_Sandino.png.351x170_q85_crop-center.jpg"'
        )
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_changed += 1

print(f"Fixed sidebar wrapper and image in {files_changed} files.")
