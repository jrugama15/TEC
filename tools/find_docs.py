import glob
import os

logs = glob.glob(r'C:\Users\Jose\.gemini\antigravity\brain\e17ca7cb-154c-4ca9-a6c4-c4f5b5617d9c\.system_generated\logs\*.txt')
logs.sort(key=os.path.getmtime, reverse=True)

found = False
for f in logs:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        log = fp.read()
        if 'Los 5 documentos' in log or 'Los 5 documentos más recientes extraídos' in log or 'documentos como antes' in log:
            idx = log.rfind('<!-- SECCION MULTIMEDIA -->')
            if idx != -1:
                print('FOUND HTML IN LOG!')
                end = log.find('<!-- SECCION GALERIA DESTACADA -->', idx)
                if end != -1:
                    print(log[idx:end])
                else:
                    print(log[idx:idx+3500])
                found = True
                break

if not found:
    print("Could not find the HTML snippet in logs")
