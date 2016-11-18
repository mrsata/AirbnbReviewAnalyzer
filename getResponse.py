import requests
import json
import io
import pymongo 
from contextlib import suppress

client = pymongo.MongoClient('localhost', 27017)
_DEBUG = False
def send_request(offset, listing_id, limit=50):
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
                "_limit": str(limit),
                "_offset": str(offset),
                "_order": "language",
                #"listing_id": "2056659",
                "listing_id": str(listing_id),#"7762953",
                "role": "all",
            },
        )

        if _DEBUG:
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                 content=response.content))

        return response.json()

    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def get_all_requests(listing_id):
    resp = send_request(0, listing_id)
    reviews_count = resp['metadata']['reviews_count']
    reviews = resp['reviews']
    for offset in range(50, reviews_count, 50):
        new_resp = send_request(offset, listing_id)
        reviews.extend(new_resp['reviews'])
    def syncID(d):
        id_num = d['id']
        del d['id']
        d['_id'] = id_num
        return d
    reviews = list(map(syncID,reviews))
    return reviews

def main():
    resp = get_all_requests(7762953)
    data = resp
    db = client.ara
    collection = db.reviews
    with suppress(Exception):
        collection.insert_many(data, ordered=False)
    if _DEBUG:
        with open('data.json', 'w') as f:
           json.dump(data, f, indent = 4, separators = (',', ':'))
if __name__ == '__main__':
    main()