import os
import nltk
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import *

ps = PorterStemmer()

def build_idf(document):
	idf = {}
	stopwords = set(open("stopwords.txt").read().split())
	for word in document:
		word = word.lower()
		if not word.strip(): continue
		if word in stopwords: continue
		word = ps.stem(word)
		if word not in idf:
			idf[word] = 0
		idf[word] += 1
	num_docs = float(len(document))
	idf = {k : num_docs/v for k, v in idf.iteritems()}
	return idf

def create_corpus():
	corpus = brown.words() 
	corpus += treebank.words()
	corpus += nps_chat.words()
	corpus += abc.words()
	corpus += gutenberg.words()
	corpus += inaugural.words()
	corpus += state_union.words()
	return corpus

if __name__ == "__main__":
	corpus = create_corpus()
	idf = build_idf(corpus)
	output = ""
	for k, v in idf.iteritems():
		output += k+" "+str(v)+"\n"
	with open("idf.txt", "w") as f:
		f.write(output)