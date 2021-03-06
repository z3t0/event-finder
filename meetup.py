# This aggregator is used for meetup
# this module exports an aggregator function which is the only interface
# for public use

import util

AUTH_TOKEN = util.get_secrets()["meetup"]["token"]
BASE_URI = "https://api.meetup.com/"

CATEGORIES = "34" # Tech
LOCATION_ADDRESS = "Ottawa"
LOCATION_WITHIN = 10 # in miles


def aggregator(address=None, within=None):
    """ (string, string)
    
    Performs a search on the Meetup endpoint and returns
    a processed list of events.

    address: eg. "Ottawa"
    within: distance from the address eg "10" in miles

    """
    # Set location
    address = address or LOCATION_ADDRESS
    within = within or LOCATION_WITHIN

    # Perform search
    data = search(address=address, within=within)

    # Get events
    events = get_events(data)

    # Process
    processed = util.process_events(events, event_info)

    return processed


def search(query="", address=LOCATION_ADDRESS, within=LOCATION_WITHIN, categories = CATEGORIES):
    """ string, string, number, string -> dict

    Searches Meetup and returns a JSON dict with the results

    query: string of search parameters
    address: location eg "Ottawa" or "1200 Merivale Road", this is processed by Google Maps Geocoding API
    within: 

    """

    # Get the longitude and latitude of the given address using Google Maps'
    # Geocoding API
    lat, lon = util.get_lon_lat(address)

    # Build the request url
    uri = f"{BASE_URI}/find/upcoming_events/?topic_category={categories}&radius={within}&lat={lat}&lon={lon}&sign=true&key={AUTH_TOKEN}"

    # Perform the request
    res = util.request(uri)

    return res


def get_events(data):
    """ dict -> list
    
    Return the events from a Meetup request

    """

    return data["events"]

def event_info  (event):

    """ dict -> dict

    Takes an event from MeetUp and extracts the relevant information. 
    The results from MeetUp is not always consistent, hence the if statements.

    """


    # Comments; Meetup's API is fairly inconsistent and does not defined required fields
    # It may also return data that is incomplete depending on the membership status of the requester

    info = {
        "name": event["name"],
        "url": event["link"]
    }

    if "description" in event:
        info["description"] = event["description"]

    if "date" in event:
        info["date"] = event["local_date"]

    return info
