import re

with open('../pages/eventos.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'(<div class="row g-4">).*?(<nav aria-label)', text, re.DOTALL)
if match:
    print('FOUND')
else:
    print('NOT FOUND')
