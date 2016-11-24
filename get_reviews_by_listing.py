import gevent
import requests
import json
import io
import pymongo 
from contextlib import suppress

DEBUG = False
SAMPLE = 7762953 # Chris: 7762953, Gilda: 2056659

def get_reviews(listing_id, offset = 0):
    # Review
    # GET https://api.airbnb.com/v2/reviews
    try:
        response = requests.get(
            url="https://api.airbnb.com/v2/reviews",
            params={
                "client_id": "3092nxybyb0otqw18e8nh5nty",
                "locale": "en-US",
                "currency": "USD",
                "_format": "for_mobile_client",
                "_limit": "50",
                "_offset": str(offset),
                "_order": "language",
                "listing_id": str(listing_id), 
                "role": "all",
            },
        )

        if DEBUG:
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                 content=response.content))

        return response.json()

    except requests.exceptions.RequestException as e:
        print('HTTP Request failed: ', e)

def get_all_reviews(listing_id):
    resp = get_reviews(listing_id)
    reviews_count = resp['metadata']['reviews_count']
    reviews = resp['reviews']
    def get_reviews_with_current_offset(offset):
        new_resp = get_reviews(listing_id, offset)
        reviews.extend(new_resp['reviews'])
    threads = [gevent.spawn(get_reviews_with_current_offset, offset)
               for offset in range(50, reviews_count, 50)]
    gevent.joinall(threads)
    def syncID(review):
        review['_id'] = review['id']
        del review['id']
        return review
    reviews = list(map(syncID,reviews))
    return reviews

def insert_reviews(listing_id, db):
    data = get_all_reviews(listing_id)
    collection = db.reviews
    with suppress(Exception):
        collection.insert_many(data, ordered=True)
    if DEBUG:
        with open('data.json', 'w') as f:
           json.dump(data, f, indent = 4, separators = (',', ':'))

def main():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.ara
    insert_reviews(SAMPLE, db)

if __name__ == '__main__':
    main()