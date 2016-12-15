import io, re, nltk
from pathlib import Path
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.sentiment import vader as vader

SAMPLES = ['hollywood', 'venice', 'oakland', 'manhattan', 'brooklyn']

def analysis(reviews_collection_text):
	with open('data/reviews_%s' % reviews_collection_text, 'r') as f:
		raw_data = f.read()
	with open('data/reviews_%s' % reviews_collection_text, 'r') as f:
		comments = f.readlines()
	data = raw_data.replace('\n', ' ')
	data_lower = data.lower()
	tokens_with_punc = word_tokenize(data_lower)
	tokens = RegexpTokenizer(r'\w+').tokenize(data_lower)
	print("--- Most frequent tokens ---\n",
		FreqDist(tokens_with_punc).most_common(15))
	print("--- Tokens without punctuation ---\n",
		FreqDist(tokens).most_common(15))
	stop = set(stopwords.words('english'))
	words = [word for word in tokens if word not in stop]
	print("--- Most frequent words ---\n", FreqDist(words).most_common(15))
	tagged = pos_tag(words)
	nouns = [word for word, pos in tagged if (pos == 'NN')]
	print("--- Most frequent nouns ---\n", FreqDist(nouns).most_common(15))
	adjts = [word for word, pos in tagged if (pos == 'JJ')]
	print("--- Most frequent adjective ---\n", FreqDist(adjts).most_common(15))
	tokns = [RegexpTokenizer(r'\w+').tokenize(comment) for comment in comments]
	lxdst = [lexical_density(token) for token in tokns if len(token) > 0]
	avgld = sum(lxdst) / len(comments)
	print("--- Average lexical density ---\n", avgld)

def lexical_density(tokens):
	return len(set(tokens)) / len(tokens)

def sentiment_generator(reviews_collection_text):
	sia = vader.SentimentIntensityAnalyzer()
	with open('data/reviews_%s' % reviews_collection_text, 'r') as f:
		comments = f.readlines()
	pos_comments = [comment for comment in comments
					if sia.polarity_scores(comment)['compound'] > 0]
	neg_comments = [comment for comment in comments
					if sia.polarity_scores(comment)['compound'] < 0]
	neu_comments = [comment for comment in comments if comment not in
					pos_comments and comment not in neg_comments]
	with open('data/reviews_%s_pos' % reviews_collection_text, 'w') as f:
		for pos_comment in pos_comments:
			f.write('%s' % pos_comment)
	with open('data/reviews_%s_neg' % reviews_collection_text, 'w') as f:
		for neg_comment in neg_comments:
			f.write('%s' % neg_comment)
	with open('data/reviews_%s_neu' % reviews_collection_text, 'w') as f:
		for neu_comment in neu_comments:
			f.write('%s' % neu_comment)

def main():
	print("\nAirbnbReviewAnalyzer v1.0")
	for reviews_collection_text in SAMPLES:
		# The following line of code generates the texts for positive comments
		# and negative comments based on nltk vader sentiment analysis.
		# ONLY RUN THIS LINE AT THE FIRST TIME to initialize the text.
		# There is no need to regenerate the text after the first run.
		# Uncomment the line below to use it:
		# sentiment_generator(reviews_collection_text)
		pos_file = Path("data/reviews_%s_pos" % reviews_collection_text)
		neg_file = Path("data/reviews_%s_neg" % reviews_collection_text)
		if pos_file.is_file() and neg_file.is_file():
			print('\nReviews with sentiment found. Implementing analysis...')
			print('------ Analysis for positive comments at %s ------'
					% reviews_collection_text)
			analysis(reviews_collection_text + "_pos")
			print('------ Analysis for negative comments at %s ------'
			% reviews_collection_text)
			analysis(reviews_collection_text + "_neg")
		else:
			print('\nSentiment analysis not done. Analyzing general reviews...')
			print('------ Analysis for %s ------' % reviews_collection_text)
			analysis(reviews_collection_text)
		print('------ Analysis for big reviews at %s ------'
		% reviews_collection_text)
		analysis(reviews_collection_text + "_big")

if __name__ == '__main__':
	main()
