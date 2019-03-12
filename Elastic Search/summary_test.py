from scroll_query import df
from processing_dataframe import processing_df
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import heapq

#set stopwords to english
stopwords = stopwords.words('english')

df2 = processing_df(df)
print(df2)