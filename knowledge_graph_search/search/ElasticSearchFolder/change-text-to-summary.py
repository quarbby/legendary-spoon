import json
from datetime import datetime
import re

file_location = "data/AI_tweets_03.json"

with open(file_location) as f:
	data = json.load(f)

for i, tweet in enumerate(data):
	data[i]['published'] = datetime.strptime(data[i]['published'], 
	"%a %b %d %H:%M:%S +0000 %Y")
	data[i]['published'] = re.sub(' ', 'T', str(data[i]['published']))


with open("data/AI_tweets_04.json", "w") as f1:
	json.dump(data, f1)