import gevent
import requests
import json
import io
import pymongo 
from contextlib import suppress

DEBUG = False
SAMPLE = 'Hollywood, LA'

def get_listings(location, _offset = 0):
    # Listing
    # GET https://api.airbnb.com/v2/search_results

    try:
        response = requests.get(
            url="https://api.airbnb.com/v2/search_results",
            params={
                "client_id": "3092nxybyb0otqw18e8nh5nty",
                "locale": "en-US",
                "currency": "USD",
                "_limit": "50",
                "_offset": str(_offset),
                "location": location,
                # "_format": "for_search_results_with_minimal_pricing",
                # "fetch_facets": "true",
                # "guests": "1",
                # "ib": "false",
                # "ib_add_photo_flow": "true",
                # "min_bathrooms": "0",
                # "min_bedrooms": "0",
                # "min_beds": "1",
                # "min_num_pic_urls": "10",
                # "price_max": "50",
                # "price_min": "10",
                # "sort": "1",
                # "user_lat": "37.3398634",
                # "user_lng": "-122.0455164",
            },
        )

        if DEBUG:
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                content=response.content))

        return response.json()

    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def get_all_listings(location):
    resp = get_listings(location)
    metadata = resp['metadata']
    metadata['location'] = location
    metadata['_id'] = metadata['geography']['place_id']
    collection = DB.metadata
    with suppress(Exception): 
        collection.insert_one(metadata)
    listings_count = metadata['listings_count']
    listings = list(map(lambda x:x['listing'], resp['search_results']))
    def get_listings_with_current_offset(offset):
        new_resp = get_listings(location, offset)
        print(offset)
        try:
            new_listings = list(map(lambda x: x['listing'], 
                                    new_resp['search_results']))
        except exceptions.KeyError:
            print('Error offset: ', offset)
        listings.extend(new_listings)
    threads = [gevent.spawn(get_listings_with_current_offset, offset)
               for offset in range(50, listings_count -50, 50)]
    gevent.joinall(threads)
    def syncID(listing):
        listing['_id'] = listing['id']
        del listing['id']
        return listing
    listings = list(map(syncID,listings))
    return listings

def insert_listings(location, db):
    global DB
    DB = db
    print("--- Start getting listings at %s ---" % location)
    data = get_all_listings(location)
    collection = db.listings
    with suppress(Exception):
        collection.insert_many(data, ordered=False)
    if DEBUG:
        with open('data.json', 'w') as f:
           json.dump(data, f, indent = 4, separators = (',', ':'))
    print("--- Finish getting listings at %s ---" % location)

def main():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.ara
    insert_listings(SAMPLE, db)

if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
