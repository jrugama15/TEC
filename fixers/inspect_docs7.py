import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.tecnacional.edu.ni/documentos/"
try:
    with urllib.request.urlopen(url, context=ctx) as response:
        html = response.read().decode('utf-8')
except Exception as e:
    print("Could not fetch documents", e)
    html = ""


idx = html.find('ADAPTACION_AL_CAMBIO')
if idx != -1:
    print(html[idx-300:idx+600])
