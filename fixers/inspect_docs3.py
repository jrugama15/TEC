import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.tecnacional.edu.ni/documentos/"
try:
    with urllib.request.urlopen(url, context=ctx) as response:
        html = response.read().decode('utf-8')
        print(html.find('col-xs-12 col-md-4 wow fadeIn'))
except Exception as e:
    print("Error:", e)
