import json
import re

with open('../data/centers.json', 'r', encoding='utf-8') as f:
    centers = json.load(f)

with open('../index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Update the button click handler to use local pages
old_handler = "window.open(centroSelect.value, '_blank');"
new_handler = """
            var slug = centroSelect.value;
            if (slug) {
              // Convert /centro/SLUG/ to centros/SLUG.html
              var parts = slug.replace(/^\\/centro\\//, '').replace(/\\/$/, '');
              window.location.href = 'centros/' + parts + '.html';
            }
          """
text = text.replace(old_handler, new_handler)

# Update the card rendering to use local links
old_link = "let link = c.url.startsWith('http') ? c.url : 'https://www.tecnacional.edu.ni' + c.url;"
new_link = "let link = 'centros/' + c.url.replace(/^\\/centro\\//, '').replace(/\\/$/, '') + '.html';"
text = text.replace(old_link, new_link)

with open('../index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated center search to use local microsites!")
