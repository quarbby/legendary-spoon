from pandas import pandas as pd
import collections
from .scroll_query import graph_query
import jieba.posseg as psg
from ..config import es
from .uploading_data import upload_data_ner


def NER_stocks(keyword):
	res = es.search(index = 'stocks', size = 10000, scroll = '2m' , body= {"query": {"match_all": {}}})
	stock_list = []
	for i in range( len(res['hits']['hits'])):
		stock_list.append(res['hits']['hits'][i]['_source'])
	
	df,_ = graph_query(keyword,'news')
	summary_list = df.summary.tolist()
	summary_string= " ".join(summary_list)
	pos_tag = psg.cut(summary_string)
	organisation_list = []

	for j in pos_tag:
		if j.flag == "nt":
			organisation_list.append(j.word)



	df1 = pd.DataFrame({'col': organisation_list})
	df2 = df1.col.value_counts(sort = True)


	companies = []
	for key,value in df2.iteritems():
		company_detail = {}
		if '公司' in key or '集团'in key:
			company_detail['name'] = key
			company_detail['count'] = value
			company_detail['label'] = keyword
			companies.append(company_detail)
	final=[]
	for i in stock_list:
		details = {}
		for j in companies:
			if j['name']==i['company_chinese']:
				details['close'] = i['close']
				details['date'] = i['date']
				details['chinese company'] = i['company_chinese']
				details['label'] =  keyword
				details['english company'] = i['company_english']
				details['count'] = j['count']
				final.append(details)
	# final = list(set(final))
	remove_duplicates = pd.DataFrame(final)
	remove_duplicates = remove_duplicates.drop_duplicates(subset='english company')
	no_duplicates = remove_duplicates.to_dict('records')
	return no_duplicates		

# items = NER_stocks('人工智能')

# upload_data_ner(items, 'stock_store')