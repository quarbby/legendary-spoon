import re
import nltk
import numpy as np
# from .dictionary import appos, emoticons, emoticons_emo
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

stopwords = stopwords.words('english')
lemma = nltk.WordNetLemmatizer()


def processing_df(df):

	#Make lower case
	df['processed'] = df['summary'].apply(lambda x: x.lower())

	# #Replace emoticons present in text with words from first dict
	# df['processed'] = df['processed'].apply(lambda x: ' '.join([emoticons[word] if word in emoticons else word for word in x.split()]))

	# #Replace emoticons present in text with words from first dict
	# df['processed'] = df['processed'].apply(lambda x: ' '.join([emoticons_emo[word] if word in emoticons_emo else word for word in x.split()]))

	# #Expand contractions
	# df['processed'] = df['processed'].apply(lambda x: ' '.join([appos[word] if word in appos else word for word in str(x).split()]))

	# #remove links
	df['processed'] = df['processed'].apply(lambda x:' '.join(re.sub('http\S+\s*', '', x).split()))
	
	#Remove hashtags, tags and numbers. Lemmatize the words
	df['no_tags'] = df['processed'].apply(lambda x: ' '.join(re.sub('#\S+', '', x).split()))
	df['no_tags'] = df['no_tags'].apply(lambda x: ' '.join(re.sub('@\S+', '', x).split()))
	df['no_tags'] = df['no_tags'].apply(lambda x: ' '.join(re.sub('[()]', '', x).split()))
	df['no_tags'] = df['no_tags'].apply(lambda x: re.sub(r"[^\w\s]", ' ', x))
	df['no_tags'] = df['no_tags'].apply(lambda x:' '.join([word for word in x.split() if word.isalpha()]))
	df['no_tags'] = df['no_tags'].apply(lambda x: ' '.join([lemma.lemmatize(word, "v")
		for word in x.split(' ')]))

	#Total length of sentence
	df['sentence_length'] = df['processed'].apply(lambda x: len(x)).astype(float)

	#Total number of words
	df['number_words'] = df['processed'].apply(lambda x: len(x.split(' '))).astype(float)

	#Total number of words that are not stopwords
	df['number_not_stopword'] = df['processed'].apply(lambda x: len([t for t in x.split(' ')
		if t not in stopwords])).astype(float)

	#Get average word length
	df['average_word_length'] = df['processed'].apply(lambda x: np.mean([len(t) for t in x.split(' ') if t not in stopwords])
        if len([len(t) for t in x.split(' ') if t not in stopwords]) > 0 else 0).astype(float)

	#Remove stopwords
	df['no_stopwords_duplicate'] = df['no_tags'].apply(lambda x: ' '.join([word for word in x.split() if word not in stopwords]))

	#remove any duplicate letter that appears more than 2 times in a word
	df['no_stopwords_duplicate'] = df['no_stopwords_duplicate'].str.replace(r'(\w)\1{%d,}'%(3-1), r'\1')

	#To get the year published
	df['published_year'] = df['published'].apply(lambda x:  ' '.join(re.sub('-\S+', '', x).split()))

	#To get the date without time published
	df['published_date'] = df['published'].apply(lambda x:  ' '.join(re.sub('T\S+', '', x).split()))

	return(df)