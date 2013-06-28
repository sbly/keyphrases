import os
import nltk
import re
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def build_idf(document):
	idf = {}
	stopwords = set(open("stopwords.txt").read().split())
	for word in document:
		word = word.lower()
		if word in stopwords: continue
		word = ps.stem(word)
		if word not in idf:
			idf[word] = 0
		idf[word] += 1
	num_docs = float(len(document))
	idf = {k : num_docs/v for k, v in idf.iteritems()}
	return idf


if __name__ == "__main__":
	docs = nltk.corpus.brown.words()
	# for i in os.listdir("out"):
	# 	for j in os.listdir("out/"+i):
	# 		for f in os.listdir("out/"+i+"/"+j):
	# 			docs.add(open("out/"+i+"/"+j+"/"+f).read())
	idf = build_idf(docs)
	output = open("idf.txt", "w")
	for k, v in idf.iteritems():
		output.write(k+" "+str(v)+"\n")
	output.close()