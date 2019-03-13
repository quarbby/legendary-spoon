"""
Config File consists of the following:
1) Location of data file to be uploaded.
2) Connection to Elastic Search
"""
from elasticsearch import Elasticsearch

"""
Change the param to where your data set is.
Example: location = 'D:/test/scholar_paper_02.json'
"""
location = 'D:/test/scholar_paper_02.json'

"""
Establish connection to Elastic search
"""
es = Elasticsearch([{'host' : 'localhost', 'port' : 9200}])