import requests
import json
import io
import pymongo 
import gevent
from contextlib import suppress

DEBUG = False
SAMPLE = 'Hollywood, LA'
CLIENT = pymongo.MongoClient('localhost', 27017)

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
                # "price_max": "210",
                # "price_min": "40",
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
    listings_count = resp['metadata']['listings_count']
    listings = list(map(lambda x: x['listing'], resp['search_results']))
    def get_listings_with_current_offset(offset):
        new_resp = get_listings(location, offset)
        print(offset)
        try:
            new_listings = list(map(lambda x: x['listing'], new_resp['search_results']))
        except exceptions.KeyError:
            print('Error offset: ', offset)
        listings.extend(new_listings)
    threads = [gevent.spawn(task, offset) for offset in range(50, listings_count - 50, 50)]
    gevent.joinall(threads)
    def syncID(listing):
        id_num = listing['id']
        del listing['id']
        listing['_id'] = id_num
        return listing
    listings = list(map(syncID,listings))
    return listings

def insert_listings(location):
    data = get_all_listings(location)
    db = CLIENT.ara
    collection = db.listings
    with suppress(Exception):
        collection.insert_many(data, ordered=False)
    if DEBUG:
        with open('data.json', 'w') as f:
           json.dump(data, f, indent = 4, separators = (',', ':'))

def main():
    import timeit
    print(timeit.timeit("insert_listings(SAMPLE)"))

if __name__ == '__main__':
    main()