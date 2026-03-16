import os
import glob
log_files = glob.glob(r'C:\Users\Jose\.gemini\antigravity\brain\e17ca7cb-154c-4ca9-a6c4-c4f5b5617d9c\.system_generated\logs\*.txt')
log_files.sort(key=os.path.getmtime, reverse=True)
for f in log_files:
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            c = file.read()
            if 'MULTIMEDIA Y DOCUMENTOS' in c and '<h6 class="fw-bold mb-3"' in c:
                print('Found in', f)
                idx = c.find('MULTIMEDIA Y DOCUMENTOS')
                print(c[idx:idx+3000])
                break
    except:
        pass
