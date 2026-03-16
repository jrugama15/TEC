import json
from collections import defaultdict

with open('../data/careers.json','r',encoding='utf-8') as f:
    careers = json.load(f)

grouped = defaultdict(lambda: defaultdict(list))
for c in careers:
    grouped[c['macro_sector']][c['sector_name']].append(c)

for macro in ['industria','comercio','agropecuario']:
    print(macro + ':')
    for sector, cs in grouped[macro].items():
        print('  ' + sector + ': ' + str(len(cs)) + ' carreras')
