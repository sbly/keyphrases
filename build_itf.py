import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import *

ps = PorterStemmer()
stopwords = set(open("stopwords.txt").read().split())

def build_idf(document, grams):
	idf = {}
	for sent in document:
		sent = preprocess(sent)
		if not sent: continue
		for n in range(grams): 
			for i in range(len(sent)):
				window = tuple(sent[i:i+n+1])
				if window not in idf:
					idf[window] = 0
				idf[window] += 1
	num_docs = float(len(document))
	idf = {k : num_docs/v for k, v in idf.iteritems()}
	return idf

def create_corpus_words():
	corpus = brown.words() 
	corpus += treebank.words()
	corpus += nps_chat.words()
	corpus += abc.words()
	corpus += gutenberg.words()
	corpus += inaugural.words()
	corpus += state_union.words()
	return corpus

def create_corpus_sents():
	corpus = brown.sents() 
	corpus += treebank.sents()
	return corpus

def preprocess(sentence):
	sentence = [word.lower().strip() for word in sentence]
	sentence = [ps.stem(word) for word in sentence if word not in stopwords]
	return sentence

if __name__ == "__main__":
	corpus = create_corpus_sents()
	idf = build_idf(corpus, 2)
	output = ""
	for k, v in idf.iteritems():
		output += " ".join(list(k))+"\t"+str(v)+"\n"
	with open("idf.txt", "w") as f:
		f.write(output)