import pymongo
import json
import io
import re

SAMPLES = ['hollywood', 'venice', 'oakland', 'manhattan', 'brooklyn']

def reviews_to_text(reviews_colle, db):

	reviews_cursor = db['reviews_' + reviews_colle].find()
    reviews = [review for review in reviews_cursor]
	comments = []
	for i in xrange(0,len(rvws)):    
		comment = rvws[i]["comments"]
		comment = re.sub('\s+', ' ', comment)
		comments.append(comment)

	with open('data/reviews_%s' % reviews_colle, 'w') as f:
		for comment in comments:
			f.write('%s\n' % comment)

def main():
	# client = pymongo.MongoClient('localhost', 27017)
	# db = client.ara
	# for reviews_colle in SAMPLES:
	# 	reviews_to_text(reviews_colle, db)
	with open('data/cmt','r') as f:
		print(f.)

if __name__ == '__main__':
	main()