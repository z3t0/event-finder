# This aggregator is used for eventbrite
# this module exports an aggregator function which is the only interface
# for public use

import util

OAUTH_TOKEN = util.get_secrets()['eventbrite']['token']
BASE_URI = "https://www.eventbriteapi.com/v3/events/search/"

LOCATION_ADDRESS = "Ottawa"
LOCATION_WITHIN = "100km"
CATEGORIES = "102" # Science and Technology
START_DATE_RANGE_START = util.now()

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
    

def search (query="", address=LOCATION_ADDRESS, within=LOCATION_WITHIN, date=START_DATE_RANGE_START, categories = CATEGORIES):
    """ string, string, string, string, string) -> dict
    
    Searches EventBrite and returns a JSON dict with the results
    
    query: string of search parameters
    address: string of address
    within: string of distance from address eg. "100km"
    date: datetime-tz string of start date
    categories: string of category ids specified in EventBrite's API

    """

    page = 1
    events = {"events": []}

    while True:
        # Build the request uri
        uri = f"{BASE_URI}?q={query}&page={page}&location.address={address}&location.within={within}&start_date.range_start={START_DATE_RANGE_START}&categories={categories}&token={OAUTH_TOKEN}"

        res = util.request(uri)

        if "events" in res:
            events["events"].extend(res["events"])
        else:
            print("Error on request")

        max_page = res["pagination"]["page_count"]

        if (max_page == page): 
            break

        page = page + 1

    return events

def get_events (data):
    """ dict -> list

    Returns the events from an EventBrite request that returns a paginated list of event objects

    """

    return data["events"]

def event_info (event):
    """ dict -> dict
    
    Takes an event dictionary, as provided by EventBrite's API
    and extracts the information into a more consistent spec.

    """

    ## TODO: description has wierd formatting, might just be unicode symbols and mismatched return characters
    
    info = {
        "name": event["name"]["text"],
        "description": event["description"]["text"],
        "url": event["url"],
        "date": event["start"]["local"],
        "is_free": event["is_free"]
    }

    return info
