from ..config import es
from pandas import pandas as pd
import collections
from .scroll_query import text_query
from pprint import pprint
import jieba.posseg as psg
import json
import googlemaps
import requests

def find_NER(keyword):
	p = text_query(keyword,'news', dataframe = True)
	words = p.summary.tolist()
	publisher = p.author.tolist()
	wordList = []

	for i in range (len(words)):
		wordList.append(psg.cut(words[i]))
	
	pos_tag = []
	publisher_list = []
	for j in range (len(wordList)):
		for i in wordList[j]:
			if i.flag == "nt":
				pos_tag.append(i.word)
				publisher_list.append(publisher[j])
	Authorcount = collections.Counter(pos_tag)

	intemediate_list = pd.DataFrame({"publisher": publisher_list, "mention_company": pos_tag})
	dicAuthorcount = dict(Authorcount)

	Final_List = []
	for key,values in dicAuthorcount.items():
		final = dict()
		x = []
		final['company'] = key 
		final['count'] = values
		final['label'] = keyword

		for j in range (len(pos_tag)):
			if key == intemediate_list['mention_company'][j]:
				if intemediate_list['publisher'][j] not in x:
					x.append(intemediate_list['publisher'][j])
		final['publisher_companies'] = x
		Final_List.append(final)

####################################### Import To GoogleMAPs ###########################################3



	gmaps = googlemaps.Client(key='AIzaSyCHC6rS5ps845uN757_to_Py401MayV898')
	# pprint(Final_List[0])
	LABELS = Final_List[0]['label']

	## For publisher
	Publisher = []
	for i in range (len(Final_List)):
		for j in Final_List[i]['publisher_companies']:
			Publisher.append(j)


	Final_Lists = []
	names = []
	for i in range (len(Final_List)):
		intemediate = dict()
		
		if Publisher[i] not in names:
			count = Publisher.count(Publisher[i])

			intemediate['publisher'] = Publisher[i]
			names.append(Publisher[i])
			intemediate['weight'] = count
			Final_Lists.append(intemediate)

	companies = []
	weighting = []
	for i in range (len(Final_Lists)):
		if '网' not in Final_Lists[i]['publisher'] and '.com' not in Final_Lists[i]['publisher'] and '.NET' not in Final_Lists[i]['publisher'] and '.COM' not in Final_Lists[i]['publisher']:
			if Final_Lists[i]['publisher'] not in companies:
				companies.append(Final_Lists[i]['publisher'])
				weighting.append(Final_Lists[i]['weight'])	
	
	## For other companies
	Total = []
	for i in range (len(Final_List)):
		y = dict()
		y['publisher'] = Final_List[i]['company']
		y['weighting'] = Final_List[i]['count']
		Total.append(y)

	Government = []
	for j in range(len(Total)):
		if '国际' in Total[j]['publisher'] or '局' in Total[j]['publisher'] or '政府' in Total[j]['publisher'] or '委' in Total[j]['publisher']:
			Government.append(Total[j])
	
	Companies = []
	for j in range(len(Total)):
		if '公司' in Total[j]['publisher'] or '集团' in Total[j]['publisher'] or '中' in Total[j]['publisher'] or '银行' in Total[j]['publisher'] or '卫视' in Total[j]['publisher'] or '新旗舰'in Total[j]['publisher']:
			if Total[j]['publisher'] not in (Government[k]['publisher'] for k in range (len(Government))):
				Companies.append(Total[j])

	Education = []
	for j in range(len(Total)):
		if '学' in Total[j]['publisher'] or  '院' in Total[j]['publisher']:
			if Total[j]['publisher'] not in (Government[k]['publisher'] for k in range (len(Government))) and Total[j]['publisher'] not in (Companies[k]['publisher'] for k in range (len(Companies))):
				Education.append(Total[j])


	FinalIP = []
	print("initializing GoogleMAPs.....")
	for j in range (len(companies)):
		IP = dict()
		locations = gmaps.geocode(companies[j])
		if locations != []:
			IP['weighting'] = weighting[j]
			IP['publisher'] = companies[j]
			IP['Address'] = locations
			IP['types'] = 'news'
			IP['labels'] = LABELS
			FinalIP.append(IP)

	for j in range (len(Government)):
		IP = dict()
		locations = gmaps.geocode(Government[j]['publisher'])
		if locations != []:
			IP['weighting'] = str(Government[j]['weighting'])
			IP['publisher'] = Government[j]['publisher']
			IP['Address'] = locations
			IP['types'] = 'Government_Sectors'
			IP['labels'] = LABELS
			FinalIP.append(IP)

	for j in range (len(Companies)):
		IP = dict()
		locations = gmaps.geocode(Companies[j]['publisher'])
		if locations != []:
			IP['weighting'] = str(Companies[j]['weighting'])
			IP['publisher'] = Companies[j]['publisher']
			IP['Address'] = locations
			IP['types'] = 'Private_Companies'
			IP['labels'] = LABELS
			FinalIP.append(IP)
	print("Almost done")
	for j in range (len(Education)):
		IP = dict()
		locations = gmaps.geocode(Education[j]['publisher'])
		if locations != []:
			IP['weighting'] = str(Education[j]['weighting'])
			IP['publisher'] = Education[j]['publisher']
			IP['Address'] = locations
			IP['types'] = 'Institutions'
			IP['labels'] = LABELS
			FinalIP.append(IP)

	print('Finish')
	return (FinalIP)




