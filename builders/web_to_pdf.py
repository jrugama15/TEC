import os
import glob
import subprocess
from PyPDF2 import PdfMerger

def export_to_pdf(html_path, pdf_path):
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"Error printing {html_path}: {e}")
        return False

def main():
    base_dir = r"d:\Respaldo José Rugama\Escritorio\Tecnologico Nacional 2026"
    os.chdir(base_dir)
    
    # 1. Gather all main files (avoiding hundreds of centros/carreras which might take hours, but let's grab the main ones)
    files = []
    if os.path.exists('index.html'):
        files.append(os.path.abspath('index.html'))
    
    pages_dir = os.path.join(base_dir, 'pages')
    if os.path.exists(pages_dir):
        pages = glob.glob(os.path.join(pages_dir, '*.html'))
        files.extend([os.path.abspath(p) for p in pages])
    
    temp_pdfs = []
    print(f"Generando {len(files)} PDFs individuales. Esto puede demorar unos minutos...")
    
    for i, file in enumerate(files):
        print(f"[{i+1}/{len(files)}] {os.path.basename(file)}...")
        out_pdf = os.path.abspath(f"temp_{i}.pdf")
        
        # Windows edge needs file:/// or absolute path
        file_uri = "file:///" + file.replace("\\", "/")
        if export_to_pdf(file_uri, out_pdf):
            temp_pdfs.append(out_pdf)
            
    if not temp_pdfs:
        print("No se pudo generar ningún PDF.")
        return
        
    print("Combinando todos los PDFs en un solo archivo...")
    merger = PdfMerger()
    for pdf in temp_pdfs:
        try:
            merger.append(pdf)
        except Exception as e:
            print(f"Saltando PDF roto {pdf}")

    final_output = os.path.abspath("Toda_La_Web.pdf")
    merger.write(final_output)
    merger.close()
    
    # Cleanup temps
    for pdf in temp_pdfs:
        try:
            os.remove(pdf)
        except:
            pass
            
    print(f"¡Terminado! Se ha generado el archivo PDF unificado en:\n{final_output}")

if __name__ == "__main__":
    main()
