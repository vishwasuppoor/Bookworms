# this script creates top keywords from the description of each book using tf-idf and store those keywords in a txt file
# books' isbn as one column and their corresponding keywords in other column

import sys
import json
import gensim
from gensim import models
from gensim import corpora
from gensim import similarities
from nltk.tokenize import word_tokenize
import pandas as pd

# input arguments are - imput json file and output keywords file respectively
file_name = sys.argv[1]
output_file = sys.argv[2]

# loading the data
json_data=open(file_name).read()
data = json.loads(json_data)
top_keywords = open(output_file,'w+')

# extracting description for every book
descriptions = {}

for data_point in data:
	for book in data[data_point]["books"]:
		descriptions[str(data[data_point]["books"][book]["isbn"])] = str(data[data_point]["books"][book]["description"])

all_descriptions = []

for isbn in descriptions:
	all_descriptions.append(str(descriptions[isbn]))

dat = pd.Series(all_descriptions)
dat = dat.apply(lambda x: str(x).lower()) 
dat = dat.apply(lambda x: word_tokenize(x))

dictionary = corpora.Dictionary(dat)
corpus = [dictionary.doc2bow(doc) for doc in dat]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

#creating keywords for every books using their respective descriptions
for isbn, description in descriptions.items():
	query_text = description
	query_text = query_text.lower()
	query_text = word_tokenize(query_text)
	vec_bow = dictionary.doc2bow(query_text)
	vec_tfidf = tfidf[vec_bow]
	sorted_vec_tfidf = sorted(vec_tfidf, key=lambda tup: tup[1], reverse=True)
	text = isbn+"\t"
	limit = 0
	if (len(sorted_vec_tfidf) >= 10):
		limit = 10
	else:
		limit = len(sorted_vec_tfidf)

	for i in range(limit):
		text = text + " " + dictionary[sorted_vec_tfidf[i][0]]
	text = text + "\n"
	top_keywords.write(text)
	
