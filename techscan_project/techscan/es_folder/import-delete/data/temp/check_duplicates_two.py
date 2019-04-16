import json
from pprint import pprint

with open("ML_weibo_07.json") as f: 
    content = json.load(f)
with open("Weibo_ML.json") as g:
    content2 = json.load(g)

print('There are {} new entries.'.format(len(content)))
print('There are {} existing unique entries.'.format(len(content2)))

total = content + content2

def unique_keys(items):
    seen = set()
    for item in items:
        key = item['summary']
        if key not in seen:
             seen.add(key)
             yield item
        else:
             pass
unique = list(unique_keys(total))

with open('Weibo_ML.json', 'w') as outfile:
    json.dump(unique, outfile)

print('Added in {} unique entries after removing {} duplicates.'.format(len(unique), len(total)-len(unique)))


