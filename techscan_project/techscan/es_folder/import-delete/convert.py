import json
import pandas as pd

location = './data/Tweets_AI_New.json'

df = pd.read_json(location)

df.to_csv(r'/Desktop/Twitter.csv')