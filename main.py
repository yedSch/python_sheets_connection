import pandas as pd
import googlemaps
import requests
import logging
import time
import sys
import csv
from importlib import reload

import unidecode
from time import sleep
import json
import numpy as np
import re
import pandas as pd
from datetime import datetime
import operator

# reload(sys)
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

data = pd.read_csv("addr.csv")

data.sort_values("Address", inplace=True)

data.drop_duplicates(subset="Address", keep=False, inplace=True)
data.sort_values(by=["ID"], ascending=True)
data.to_csv('addrFix.csv', index=False)

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

global API_KEY
API_KEY = 'AIzaSyBQjp6RoeU-XdbqLNt13qYnAAH_m4daIMk'
gmaps = googlemaps.Client(key=API_KEY)
BACKOFF_TIME = 30
output_filename = 'calculated_distances.csv'
input_filename = "addrFix.csv"
lat_column_name = "latitude"
lon_column_name = "longitude"
address_column_name = "Address"
RETURN_FULL_RESULTS = False

data = pd.read_csv(input_filename, encoding='utf8')

if address_column_name not in data.columns:
    raise ValueError("Missing Address column in input data")

addresses = data[address_column_name].tolist()


# ------------------	FUNCTION DEFINITIONS ------------------------

def get_google_results(address, api_key=None, return_full_response=False):
    """
    Get geocode results from Google Maps Geocoding API.

    Note, that in the case of multiple google geocode reuslts, this function returns details of the FIRST result.

    @param address: String address as accurate as possible. For Example "18 Grafton Street, Dublin, Ireland"
    @param api_key: String API key if present from google.
                    If supplied, requests will use your allowance from the Google API. If not, you
                    will be limited to the free usage of 2500 requests per day.
    @param return_full_response: Boolean to indicate if you'd like to return the full response from google. This
                    is useful if you'd like additional location details for storage or parsing later.
    """

    address = address.encode('utf-8')

    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?language=iw&address={}".format(address).encode(
        'utf8')
    if api_key is not None:
        geocode_url = geocode_url + "&key={}".format(api_key)

    results = requests.get(geocode_url)
    # Results will be in JSON format - convert to dict using requests functionality
    results = results.json()

    # if there's no results or an error, return empty results.
    if len(results['results']) == 0:
        output = {
            "formatted_address": None,
            "latitude": None,
            "longitude": None,
            "accuracy": None,
            "google_place_id": None,
            "type": None,
            "postcode": None
        }
    else:
        answer = results['results'][0]
        output = {
            "formatted_address": answer.get('formatted_address'),
            "latitude": answer.get('geometry').get('location').get('lat'),
            "longitude": answer.get('geometry').get('location').get('lng'),
            "accuracy": answer.get('geometry').get('location_type'),
            "google_place_id": answer.get("place_id"),
            "type": ",".join(answer.get('types')),
            "postcode": ",".join([x['long_name'] for x in answer.get('address_components')
                                  if 'postal_code' in x.get('types')])
        }

    # Append some other details:
    output['input_string'] = address
    output['number_of_results'] = len(results['results'])
    output['status'] = results.get('status')
    if return_full_response is True:
        output['response'] = results

    return output


# ------------------ PROCESSING LOOP -----------------------------

# Ensure, before we start, that the API key is ok/valid, and internet access is ok
test_result = get_google_results("Tel Aviv, Israel", API_KEY, RETURN_FULL_RESULTS)
if (test_result['status'] != 'OK'):
    logger.warning("There was an error when testing the Google Geocoder.")
    print('Problem with test results from Google Geocode - check your API key and internet connection.')

# Create a list to hold results
results = []
# Go through each address in turn

for address in addresses:

    # While the address geocoding is not finished:
    geocoded = False
    while geocoded is not True:
        # Geocode the address with google
        try:
            geocode_result = get_google_results(address, API_KEY, return_full_response=RETURN_FULL_RESULTS)
        except Exception as e:
            logger.exception(e)
            logger.error("Major error with {}".format(address).encode('utf8'))
            logger.error("Skipping!")
            geocoded = True

        # If we're over the API limit, backoff for a while and try again later.
        if geocode_result['status'] == 'OVER_QUERY_LIMIT':
            logger.info("Hit Query Limit! Backing off for a bit.")
            time.sleep(BACKOFF_TIME * 60)  # sleep for 30 minutes
            geocoded = False
        else:
            # If we're ok with API use, save the results
            # Note that the results might be empty / non-ok - log this
            if geocode_result['status'] != 'OK':
                logger.warning("Error geocoding {}: {}".format(address, geocode_result['status']))
            logger.debug("Geocoded: {}: {}".format(address, geocode_result['status']))
            results.append(geocode_result)
            geocoded = True

    # Print status every 100 addresses
    if len(results) % 100 == 0:
        logger.info("Completed {} of {} address".format(len(results), len(addresses)))

    # Every 500 addresses, save progress to file(in case of a failure so you have something!)
    if len(results) % 500 == 0:
        pd.DataFrame(results).to_csv("{}_bak".format(output_filename))

# All done
logger.info("Finished geocoding all addresses")
# Write the full results to csv using the pandas library.
pd.DataFrame(results).to_csv(output_filename, encoding='utf8')

# Check distance and travel time
data = pd.read_csv("calculated_distances.csv")

data.sort_values("formatted_address", inplace=True)

data.drop_duplicates(subset="formatted_address", keep=False, inplace=True)
data.sort_values(by=["formatted_address"], ascending=True)
data.to_csv('calculated_distances.csv', index=False)

input_filename2 = "calculated_distances.csv"

data2 = pd.read_csv(input_filename2, encoding='utf8')
address_column_name2 = 'formatted_address'
if address_column_name2 not in data2.columns:
    raise ValueError("Missing Address column in input data2")
addr = data2[address_column_name2].tolist()
for address in addr:
    # current location address input
    currentLocation = 'Tel Aviv'

    # destination address input
    destination = address

    # base url
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    # get response
    r = gmaps.distance_matrix(currentLocation, destination, mode='driving', language='iw', avoid=None, units='metric',
                              departure_time=None)

    # return time and distance as text and as seconds

    time = r["rows"][0]["elements"][0]["duration"]["text"]
    seconds = r["rows"][0]["elements"][0]["duration"]["text"]
    distance = r["rows"][0]["elements"][0]["distance"]["text"]

    # Create list with data and output to csv
    res = {'address': [address.encode('utf-8')], 'time': [time], 'distance': [distance],
           'Date': [datetime.today().strftime('%Y-%m-%d')]}
    Nres = pd.DataFrame.from_dict(res)
    pd.DataFrame(Nres).to_csv('route.csv', mode='a', encoding='utf-8-sig')
    csvf = csv.reader(open('route.csv'), delimiter=';')
    sortedlist = sorted(csvf, key=operator.itemgetter(0), reverse=False)


def write_csv():
    df2 = pd.DataFrame()
    for name, df in data.items():
        df2 = df2.append(df)
    df2.to_csv('route.csv')


print('route.csv ready!')