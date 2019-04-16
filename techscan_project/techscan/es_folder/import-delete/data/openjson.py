import json
from pprint import pprint

with open("News.json") as f: 
    content = json.load(f)
pprint((content[1]))
