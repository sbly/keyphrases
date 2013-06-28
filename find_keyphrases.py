import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import *
import operator
import string

ps = PorterStemmer()
stopwords = set(open("stopwords.txt").read().split())

def build_tf(document, grams):
	tf = {}
	sentences = nltk.sent_tokenize(document.strip())
	sentences = [nltk.word_tokenize(s) for s in sentences]
	#tagged = nltk.tag.batch_pos_tag(sentences)
	for sent in sentences:
		sent = [word for word in sent if word not in string.punctuation]
		sent = [word.lower().strip() for word in sent]
		sent = [ps.stem(word) for word in sent if word not in stopwords]
		for n in range(grams):
			for i in range(len(sent)):
				window = tuple(sent[i:i+n+1])
				if window not in tf:
					tf[window] = 0
				tf[window] += 1
	return tf

def build_tf_idf(tf, idf):
	max_score = max(idf.values())
	for word in tf:
		if word not in idf:
			idf[word] = max_score
	return {word : count*idf[word] for word, count in tf.iteritems()}

def read_idf(path):
	idf = {}
	for line in open(path):
		try: words, score = line.split("\t")
		except: continue
		words = tuple(words.split())
		idf[words] = score
	return idf

def find_keywords(text, idf):
	tf = build_tf(text, 2)
	tf_idf = build_tf_idf(tf, idf)
	tf_idf = sorted(tf_idf, key=tf_idf.get, reverse=True)
	return tf_idf[:4]

# list of (clip, correct labels, guess labels)
def evaluate(clips):
	score = 0.0
	for (clip, correct, guesses) in clips:
		print "Clip:", clip
		print "Length:", len(clip)
		print "Generated options:", guesses
		print "Number of options:", len(guesses)
		print "Labels:", correct
		intersection = set(guesses) & set(correct)
		print "Score:",
		if intersection:
			score += 1
			print 1
		else: 
			print 0
		print
	print "Overall score:", score/len(clips)

def test1():
	clips = []
	for line in open("clipper_data/selected_labels.txt"):
		parts = line.split("\t")
		print "Clip:", parts[1],
		print "Human label:", parts[0]
		print "Machine labels:",
		keywords = set(find_keywords(parts[1], idf))
		clips.append((parts[1], parts[0], keywords))
		for word in parts[1].split():
			if not keywords: break
			word2 = ps.stem(word.lower())
			if word2 in keywords:
				print word + ",",
				keywords.remove(word2)
		print "\n"
	evaluate(clips)

def test2():
	clips = []
	for line in open("clipper_data/GoldStandardLabels.txt").read().split("\r"):
		labels, clip = line.split("\t")[:2]
		labels = labels.split()
		print "Clip:", clip
		print "Human labels:", labels
		keywords = set(find_keywords(clip, idf))
		print "Machine labels:", keywords
		labels = [ps.stem(word.lower()) for word in labels]
		clips.append((clip, labels, keywords))
		for word in clip.split():
			if not keywords: break
			word2 = ps.stem(word.lower())
			if word2 in keywords:
				print word + ",",
				keywords.remove(word2)
		print "\n"
	evaluate(clips)

def tomato_test():
	clips = []
	for line in open("clipper_data/tomatoes.txt").read().split("\n\n"):
		line = line.split("\n")
		label = line.pop(0)
		for clip in line:
			print "Clip:", clip
			print "Option:", label
			keywords = set(find_keywords(clip, idf))
			print "Machine labels:", keywords
			clips.append((clip, [label], keywords))
			# for word in clip.split():
			# 	if not keywords: break
			# 	word2 = ps.stem(word.lower())
			# 	if word2 in keywords:
			# 		print word + ",",
			# 		keywords.remove(word2)
			print "\n"
	evaluate(clips)

def build_idf(document, grams):
	idf = {}
	for sent in document:
		sent = [word for word in sent if word not in string.punctuation]
		sent = [word.lower().strip() for word in sent]
		sent = [ps.stem(word) for word in sent if word not in stopwords]
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

def write_idf():
	corpus = create_corpus_sents()
	idf = build_idf(corpus, 2)
	idf = sorted(idf.iteritems(), key=operator.itemgetter(1))
	output = ""
	for k, v in idf:
		output += " ".join(list(k))+"\t"+str(v)+"\n"
	with open("idf.txt", "w") as f:
		f.write(output)

if __name__ == "__main__":
	# write_idf()
	idf = read_idf("idf.txt")
	tomato_test()