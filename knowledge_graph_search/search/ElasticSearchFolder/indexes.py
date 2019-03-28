#Contains a list of indexes that will be used for queries
# indexes = ['scholar', 'news', 'news_test']
from ..config import es

indexes = []

res = es.indices.get_alias().keys()
for key in res:
	indexes.append(str(key))