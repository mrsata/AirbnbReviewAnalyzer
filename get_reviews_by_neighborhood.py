import pymongo
import json
import io

SAMPLES = ['hollywood', 'venice', 'oakland', 'manhattan', 'brooklyn']

def insert_reviews(neighborhood, db):
    listings_cursor = db['listings_' + neighborhood].find({"reviews_count": {"$gt": 0}})
    listings = [listing for listing in listings_cursor]
    collection = db['reviews_' + neighborhood]
    for listing in listings:
        reviews_cursor = db.reviews_en.find({'listing_id':listing['_id']})
        reviews = [review for review in reviews_cursor]
        if reviews:
            try:
                collection.insert_many(reviews, ordered=True)
            except:
                print(reviews)
                raise

def main():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.ara
    for neighborhood in SAMPLES:
        insert_reviews(neighborhood, db)

if __name__ == '__main__':
    main()