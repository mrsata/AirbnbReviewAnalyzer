import requests
import json
import io
import pymongo 
from contextlib import suppress
import get_listings_by_location.py
import get_reviews_by_listing.py

SAMPLES = ['Hollywood, LA', 'Venice, LA', 'Oakland, SF', 'Manhattan, NYC', 'Brooklyn, NYC']
CLIENT = pymongo.MongoClient('localhost', 27017)

def main():

	for sample in SAMPLES:
		insert_listings(sample)

	db = CLIENT.ara
	listings = db.listings.find()

	for listing in listings:
		insert_reviews(listing)

if __name__ == '__main__':
	main()