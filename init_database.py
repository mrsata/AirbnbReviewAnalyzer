import gevent
import gevent.monkey
gevent.monkey.patch_all()
import requests
import json
import io
import pymongo
import time
from contextlib import suppress
import get_listings_by_location as l
import get_reviews_by_listing as r

SAMPLES = ['Hollywood, LA', 'Venice, LA', 'Oakland, SF', 'Manhattan, NYC', 'Brooklyn, NYC']
CLIENT = pymongo.MongoClient('localhost', 27017)
DB = CLIENT.ara

def init_database():

    print("--- Start getting listings ---")
    listings_threads = [gevent.spawn(l.insert_listings, sample) 
                        for sample in SAMPLES]
    gevent.joinall(listings_threads)

    print("--- Get all listings: %s seconds ---" 
          % (time.time() - start_time))
    listings = DB.listings.find({"reviews_count": {"$gt": 0}})

    print("--- Start getting reviews ---")
    reviews_threads = [gevent.spawn(r.insert_reviews, listing['_id']) 
                       for listing in listings]
    gevent.joinall(reviews_threads)
    print("--- Get all reviews: %s seconds ---"
          % (time.time() - start_time))

def main():
    init_database()

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- Finished in: %s seconds ---" % (time.time() - start_time))
