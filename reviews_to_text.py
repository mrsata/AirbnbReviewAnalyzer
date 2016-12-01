import pymongo, io, re

SAMPLES = ['hollywood', 'venice', 'oakland', 'manhattan', 'brooklyn']

def reviews_to_text(reviews_collection, db):

	reviews_cursor = db['reviews_' + reviews_collection].find()
	reviews = [review for review in reviews_cursor]
	comments = [review["comments"] for review in reviews]
	comments = [comment for comment in comments 
				if 'This is an automated posting.' not in comment]
	comments = [re.sub('\s+', ' ', comment) for comment in comments]

	with open('data/reviews_%s' % reviews_collection, 'w') as f:
		for comment in comments:
			f.write('%s\n' % comment)

def main():
	client = pymongo.MongoClient('localhost', 27017)
	db = client.ara
	for reviews_collection in SAMPLES:
		reviews_to_text(reviews_collection, db)

if __name__ == '__main__':
	main()