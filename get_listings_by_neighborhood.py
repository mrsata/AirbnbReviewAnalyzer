import pymongo
import json
import io

SAMPLES = ['hollywood', 'venice', 'oakland', 'manhattan', 'brooklyn']

def insert_listings(db):
    listings_cursor = db['listings_' +
                         neighborhood].find({"reviews_count": {"$gt": 0}})
    listings = [listing for listing in listings_cursor]
    # in case of missing listings TODO: complete insert_listings

def insert_listings_big(neighborhood, db):
    listings_cursor = db['listings_' +
                         neighborhood].find({"reviews_count": {"$gt": 50}})
    listings = [listing for listing in listings_cursor]
    collection = db['listings_' + neighborhood + '_big']
    collection.insert_many(listings, ordered=True)

def main():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.ara
    for neighborhood in SAMPLES:
        insert_listings_big(neighborhood, db)

if __name__ == '__main__':
    main()
