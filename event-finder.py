#!/usr/bin/env python3

# This bot finds events for SCESoc
# written by Rafi Khan, VP of External Affairs

import util
import eventbrite
import meetup
import sys

if __name__ == "__main__":
    # Perform search on EventBrite
    if len(sys.argv) < 3:
        print("Insufficient number of arguments")
        print("Usage: \n\t \"event-finder address distance output\"")
    else:
        address = sys.argv[1]
        distance = sys.argv[2]
        output = sys.argv[3]

        eb = eventbrite.aggregator(address=address, within=distance)

        miles = util.kms_to_miles(float(distance[0:distance.find("k")]))
        mu = meetup.aggregator(address=address, within=miles)

        results = eb + mu

        # Write to file
        util.dump(output, results)
