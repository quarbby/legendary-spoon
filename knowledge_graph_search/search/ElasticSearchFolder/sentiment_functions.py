from pandas import DataFrame, read_csv
import pandas as pd
from processing_dataframe import processing_df
import re
import nltk
from nltk.corpus import stopwords
from gensim.utils import lemmatize
from tqdm import tqdm_notebook as tqdm
from nltk.stem.wordnet import WordNetLemmatizer
from dictionary import appos, emoticons_emo, emoticons
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.text import one_hot
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.text import Tokenizer
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
import numpy as np
from scroll_query import processing_hits, query
from ordered_set import OrderedSet as order

#location = r'/content/gdrive/My Drive/train.csv'

stopwords = stopwords.words('english')
extra = ['amp','im','u']
stopwords.extend(extra)
stop_words = set(stopwords)
lmtzr = WordNetLemmatizer()

df = pd.read_csv(r'C:/Users/admin/Desktop/train.csv', encoding='latin-1')
df['SentimentText'] = df['SentimentText'].str.replace('\d+', '')

def processing(df):

	#remove emoticons
    df['emoticons']=df['SentimentText'].apply(lambda x: ' '.join([emoticons[word] if word in emoticons else word for word in x.split()]))
    
    df['emo']=df['emoticons'].apply(lambda x: ' '.join([emoticons_emo[word] if word in emoticons_emo else word for word in x.split()]))
     
    #lowercase
    df['lower_desc'] =df['emo'].str.lower()
    
    #change appos
    df['appos']=df['lower_desc'].apply(lambda x: ' '.join([appos[word] if word in appos else word for word in x.split()]))
     
    #remove#
    df['hash']=df['appos'].apply(lambda x:' '.join(re.sub('#\S+', '', x).split()))
    
    #remove @user
    df['at']=df['hash'].apply(lambda x:' '.join(re.sub('@\S+', '', x).split()))
    
    #remove http
    df['http']=df['at'].apply(lambda x:' '.join(re.sub('http\S+\s*', '', x).split()))
    
    #remove punctuations
    df['processed'] = df['http'].apply(lambda x: re.sub(r'[^\w\s]', '', x.lower()))
    
    #remove punctuations, special characters and numerical tokens 
    df['remove']=df['processed'].apply(lambda x:' '.join( [word for word in x.split() if word.isalpha()]))
    
    #Lemmatization
    df['lemma'] = df['remove'].apply(lambda x: ' '.join([lmtzr.lemmatize(word, "v") for word in x.split(' ')]))
    
    #stopwords
    df['stop']= df['remove'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
    
    #remove any duplicate letter that appears more than 2 times in a word
    df['tweet'] =df['stop'].str.replace(r'(\w)\1{%d,}'%(3-1), r'\1')
    
    return (df)

def removetext(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])

cleaned=processing(df) 

cleaned['clear'] = cleaned['tweet'].apply(removetext)

#put cleaned content of sentiments for both poditive and negative sentiments respective
pos_sentence = cleaned[cleaned['Sentiment'] == 1]['clear'].tolist()

neg_sentence = cleaned[cleaned['Sentiment'] == 0]['clear'].tolist()

sentence = neg_sentence + pos_sentence

#counting the numer of datas with positive and negative sentiments respectively
num_1 = len(cleaned[cleaned['Sentiment'] == 1])

num_0 = len(cleaned[cleaned['Sentiment'] == 0])

#tokenised sentence in the list and place them in a word list
word_list = []

for sent in sentence:
  words = sent.split()
  word_list.extend(words)

unique_words = order(word_list)
# print(unique_words[20])
# word2ind = {}
# ind2word = {}
# word2ind['<PAD>'] = 0
# ind2word[0]='<PAD>'
# i = 1
# for word in unique_words:
#     word2ind[word] = i
#     ind2word[i] = word
#     i += 1

#remove duplicate word in the word_list
# unique_words = list(set(word_list))

#giving each word in the unique_words list a unique index in the form of key=word, value=index 
word2ind = {unique_words[i]: i+1 for i in range(len(unique_words))}

#padding which is to assign the index 0 for <PAD>
word2ind['<PAD>'] = 0

#dictionary with index as key and word as value
ind2word = dict([(value, key) for (key, value) in word2ind.items()])
# print(word2ind['hate'])
# print (ind2word[20582])
#number of words in the dictionary of unique_words


#encode the text which is to change contents of tweets from words to indexes
def encode_text(sentence):
    encode = []
    words = sentence.split(' ')
    
    for word in words:
       
        if word not in word2ind.keys() and word != '' :
            encode.append(word2ind['<PAD>'])

        elif word != '':
            encode.append(word2ind[word])
            
    return(encode)




	



# decode the indexes from indexes to words
def decode_text(text):
  return ' '.join([ind2word.get(i, '?') for i in text])

# sentence_data = []

# #encode the list of sentence into indexes
# for i in sentence:
# 	sentence_data.append(encode_text(i))

# #change the list into array
# sentence_data = np.array(sentence_data)

# num_sentiments = 2

# # pres_names = [0 for negative, 1 for positive]
# pres_names=[0.,1]
# sentence_labels = np.zeros((len(sentence_data), num_pres))

# # if it is negative it will be 1 in the 1st coulumn and 1 in 2nd column if it is positive
# sentence_labels[0:num_0, 0] = 1                    #negative
# sentence_labels[num_0: num_0 + num_1, 1] = 1       #positive

# rand_ind=np.random.choice(sentence_data.size, sentence_data.size)
# X = sentence_data[rand_ind]
# y = sentence_labels[rand_ind]

def predict(key_word):



	with CustomObjectScope({'GlorotUniform': glorot_uniform()}):

		saved_model = load_model(r'C:/Users/admin/Desktop/proj/Sentiment Analysis/keras.h5')

	df_data = query(str(key_word),'twitter')
	df_data = processing_df(df_data)
	sentences = df_data["no_stopwords_duplicate"].tolist()
	sentence_data=[]
	for i in sentences:
		sentence_data.append(encode_text(i))
			
	X = np.array(sentence_data)
	X_test = keras.preprocessing.sequence.pad_sequences(X, 
				value=word2ind['<PAD>'],
				padding='post',
				maxlen=128)
	predicted = saved_model.predict_classes(X_test)

	prediction = saved_model.predict(X_test)

	print(predicted)

	df_data['Sentiment'] =  predicted

	# num_positive = np.sum(prediction[:, 0] > prediction[:, 1])

	# num_negative = np.sum(prediction[:, 0] < prediction[:, 1])
	df_data['Sentiment'][df_data["Sentiment"] == 0] = 'negative'

	df_data['Sentiment'][df_data["Sentiment"] == 1] = 'positive'
	# print(num_positive)
	# print(num_negative)

	from textblob import TextBlob
	df_data['Sentiment2'] = df_data['processed'].apply(lambda x: TextBlob(x).sentiment)

	# df_data['Sentiment2'][df_data["Sentiment2"][0] == 0] = 'neutral'

	# df_data['Sentiment2'] [df_data["Sentiment2"][0] < 0] = 'negative'

	# df_data['Sentiment2'] [df_data["Sentiment2"][0] > 0] = 'negative'


	return(df_data)


# def predict(key_word):

# 	with CustomObjectScope({'GlorotUniform': glorot_uniform()}):

# 		saved_model = load_model(r'C:/Users/admin/Desktop/proj/Sentiment Analysis/keras.h5')

# 	df_data = query(str(key_word),'twitter')
	
# 	df_data = processing_df(df_data)
# 	print(len(df_data))
# 	df_data.dropna(subset=['no_stopwords_duplicate'])
# 	print(len(df_data))
	
# 	# df_data['no_stopwords_duplicate'] = df_data['no_stopwords_duplicate'].apply(lambda x:list(x.split()))	
# 	df_data['no_stopwords_duplicate'] = df_data['no_stopwords_duplicate'].apply(lambda x: encode_text(x))
# 	df_data['no_stopwords_duplicate'] = df_data['no_stopwords_duplicate'].apply(lambda x: np.array(x))
# 	df_data['no_stopwords_duplicate'] = df_data['no_stopwords_duplicate'].apply(lambda x: keras.preprocessing.sequence.pad_sequences(x, 
# 		value=word2ind['<PAD>'],
# 		padding='post',
# 		maxlen=128))

# 	df_data['sentiment'] = df_data['no_stopwords_duplicate'].apply(lambda x: saved_model.predict_classes(x))
# 	return(df_data)
# df =predict('machine')

# print(df.Sentiment)

