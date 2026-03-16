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
        
        # 1. Remove the Breadcrumb
        # Match from "<!-- Breadcrumb -->" to "</nav>\n\n" using non-greedy 
        new_content = re.sub(
            r'<!-- Breadcrumb -->\s*<nav aria-label="breadcrumb"[^>]*>.*?</nav>\s*',
            '',
            new_content,
            flags=re.DOTALL
        )
        
        # 2. Remove the Centro Tecnol\u00f3gico Blue Badge
        # Match the specific h6 tag
        new_content = re.sub(
            r'<h6 class="d-inline-block px-4 py-2 rounded-pill fw-bold text-white mb-3" style="background:linear-gradient\(135deg,#0d6efd 0%,#00adee 100%\);font-size:\.8rem;letter-spacing:\.1em;">\s*<i class="bi-building me-2"></i>CENTRO TECNOLÓGICO\s*</h6>\s*',
            '',
            new_content,
            flags=re.DOTALL
        )
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_changed += 1

print(f"Removed breadcrumbs and blue badges in {files_changed} files.")
