import io, re, nltk
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk import FreqDist


SAMPLES = ['hollywood', 'venice', 'oakland', 'manhattan', 'brooklyn']

def analysis(reviews_collection_text):
	with open('data/reviews_%s' % reviews_collection_text, 'r') as f:
		raw_data = f.read()
		comments = f.readlines()
	data = raw_data.replace('\n', ' ')
	data_lower = data.lower()
	tokens_with_punc = word_tokenize(data_lower)
	tokens = RegexpTokenizer(r'\w+').tokenize(data_lower)
	print(FreqDist(tokens_with_punc).most_common(15))
	print(FreqDist(tokens).most_common(15))
	stop = set(stopwords.words('english'))
	words = [word for word in tokens if word not in stop]
	print(FreqDist(words).most_common(15))
	tagged = pos_tag(words)
	nouns = [word for word, pos in tagged
		if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
	print(FreqDist(nouns).most_common(15))



def main():
	for reviews_collection_text in SAMPLES[:1]:
		print('--- Analysis for %s ---' % reviews_collection_text)
		analysis(reviews_collection_text)

if __name__ == '__main__':
	main()