import pdfkit
import os
import sys

# Get absolute path to the local HTML file to avoid path resolution errors in wkhtmltopdf
html_path = os.path.abspath("index.html")
pdf_path = os.path.abspath("index_pdfkit.pdf")

# If wkhtmltopdf is not found in PATH, pdfkit might throw an OSError. Let's handle it gracefully.
try:
    # Use options to allow local file access which is sometimes restricted
    options = {
        'enable-local-file-access': None,
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': "UTF-8",
        'no-outline': None
    }
    
    print(f"Generating PDF for {html_path}...")
    pdfkit.from_file(html_path, pdf_path, options=options)
    print(f"PDF successfully generated at {pdf_path}")
except OSError as e:
    # Most common error: wkhtmltopdf missing
    print("Error encountered:", str(e))
    print("\nwkhtmltopdf is likely not installed or not in PATH.")
    print("Please download it from https://wkhtmltopdf.org/downloads.html and install it.")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
    sys.exit(1)
