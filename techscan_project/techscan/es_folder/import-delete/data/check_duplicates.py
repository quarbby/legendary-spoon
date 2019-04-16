import json
from pprint import pprint

with open("totalTechWeb.json") as f: 
    content = json.load(f)
# with open("china_news_everything.json") as g:
#     content2 = json.load(g)

print('There are {} new entries.'.format(len(content)))
# print('There are {} existing unique entries.'.format(len(content2)))

# total = content + content2

def unique_keys(items):
    seen = set()
    for item in items:
        key = item['summary']
        if key not in seen:
             seen.add(key)
             yield item
        else:
             pass
unique = list(unique_keys(content))

with open('totalTechWeb.json', 'w') as outfile:
    json.dump(unique, outfile)

print('Added in {} unique entries after removing {} duplicates.'.format(len(unique), len(content)-len(unique)))


