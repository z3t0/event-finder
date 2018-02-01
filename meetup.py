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
    
    Performs a search on the EventBrite endpoint and returns
    a processed list of events.

    address: eg. "Ottawa"
    within: distance from the address eg "100km"

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

    """

    lat, lon = util.get_lon_lat(address)

    uri = f"{BASE_URI}/find/upcoming_events/?topic_category={categories}&lat={lat}&lon={lon}&sign=true&key={AUTH_TOKEN}"
    res = util.request(uri)

    return res


def get_events(data):

    return data["events"]

def event_info  (event):
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
