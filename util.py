# Utility functions

import json
import requests
from datetime import datetime

# Path to the file containing secrets such as the OAUTH Key
SECRETS_FILE = "secrets.json"

def request (uri):
    """ string -> dict

    Makes a request to the uri specified and returns the contents
    as a parsed json dictonary
    """
    # Get JSON data 
    r = requests.get(uri)

    return r.json()


# Read the secrets file
with open(SECRETS_FILE) as f:
   SECRETS = json.loads(f.read())
    

def get_secrets():
    """ None -> dict

    Returns a json dict containing the secrets file
    
    The following is the scheme of the secrets file:

        eventbrite:
            token
    	meetup:
    	    token
    	google:
	    token

    """

    return SECRETS

def now():
    """ None -> String
    
    Returns a string of the current datetime-tz

    """
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%dT%H:%m:%SZ")

    return formatted

def process_events (events, fn):
    """ (list, fn) -> list

    Takes a list of events as well as a function that is called on each event.
    A list is returned, which is composed of the return values from the 
    function.

    """

    aggregator = []

    for event in events:
        aggregator.append(fn(event))
        

    return aggregator

def clean_text (text):
    """ string -> string
    
    Cleans up text, which is used as an intermediate representation
    when an event's information is stored in a dictonary
    
    """
    return text.strip().replace("_", " ").capitalize()

def write_to_stream (aggregator):
    """ list -> None
    
    This function iterates over the elements of the aggregator
    and prints out each elements dictionary as key, values in a
    cleaner format.

    """
    for e in aggregator:
        for k in e:
            clean = clean_text(k)
            print(k + ":\t" + str(e[k]))
        print()

def dump(path, data):
    """ (string, Object)
    
    Writes to path the JSON representation of Object

    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def get_lon_lat(address):
    """ String -> (lon, lat)
    
    Searches up the address and returns a longitude
    and latitude.

    None is returned if the search failed

    """
    BASE_URI = "https://maps.googleapis.com/maps/api/geocode/json?"
    KEY = get_secrets()["google"]["token"]

    address = address.replace(" ", "+")

    uri = f"{BASE_URI}&address={address}&key={KEY}"
    res = request(uri)

    location = res["results"][0]["geometry"]["location"]
    
    return location["lat"], location["lng"]

def kms_to_miles (km):
    KM_PER_MILE = 0.62
    return km * KM_PER_MILE
