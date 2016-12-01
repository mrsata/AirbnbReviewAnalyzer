import gevent.monkey
gevent.monkey.patch_all()
import gevent
import requests
import pymongo
import json
import io
import time
from contextlib import suppress
import get_listings_by_location as l
import get_reviews_by_listing as r

SAMPLES = ['Hollywood, LA', 'Venice, LA', 'Oakland, SF', 'Manhattan, NYC', 'Brooklyn, NYC']
CLIENT = pymongo.MongoClient('localhost', 27017)
DB = CLIENT.ara
networking_pool = gevent.pool.Pool(size=3)
def init_database():

    print("--- Start getting listings ---")
    listings_threads = [gevent.spawn(l.insert_listings, sample, DB, networking_pool) 
                       for sample in SAMPLES]
    gevent.joinall(listings_threads)

    print("--- Get all listings: %s seconds ---" 
          % (time.time() - start_time))
    listings_cursor = DB.listings.find({"reviews_count": {"$gt": 0}})
    listings = [listing for listing in listings_cursor]
    print("--- listings length %s ---" % str(len(listings)))
    print("--- reviews length %s ---" % str())

    print("--- Start getting reviews ---")
    reviews_threads = [networking_pool.spawn(r.insert_reviews, listing['_id'], DB) 
                       for listing in listings]
    networking_pool.join()
    print("--- Get all reviews: %s seconds ---"
          % (time.time() - start_time))

def main():
    init_database()

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- Finished in: %s seconds ---" % (time.time() - start_time))
