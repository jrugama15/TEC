import re

# Read the footer from eventos.html
with open('../pages/eventos.html', 'r', encoding='utf-8') as f:
    ev = f.read()

idx = ev.find('<footer')
end = ev.find('</footer>', idx)
footer_html = ev[idx:end+9]

# Read galeria.html
with open('../pages/galeria.html', 'r', encoding='utf-8') as f:
    gal = f.read()

# Insert footer before the bootstrap script
insert_point = gal.find('<script src="static/core/js/bootstrap.bundle.min.js">')
if insert_point != -1:
    new_gal = gal[:insert_point] + '\n' + footer_html + '\n\n  ' + gal[insert_point:]
    with open('../pages/galeria.html', 'w', encoding='utf-8') as f:
        f.write(new_gal)
    print("Footer added to galeria.html!")
else:
    print("Could not find insert point!")
