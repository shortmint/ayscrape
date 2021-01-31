import logging as log

from requests_html import HTMLSession

from get_champ import get_champ
from getlinks import getlinks

log.basicConfig(level=log.INFO, format="%(levelname)s:%(module)s:%(message)s)")

# level=log.DEBUG, filename="root.log", format="%(asctime)%:%(levelname)%:%(message)%"

# Use parent page to get the link by (tier, link) tuples
tierLinkList = getlinks()

# open session
with HTMLSession() as session:

    d = 0  # select tier start section <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    maxtuple = (0, 0, 0)
    mintuple = (0, 0, 10000)
    max_columns = 0

    # Store champion data in champlist of dictionaries
    champlist = []
    # Loop through dictionary list of link
    for tier_link in tierLinkList[d:1]:  ### Temporary tier range
        with session.get(tier_link["url"]) as r:
            c = get_champ(r, tier_link)

        log.info(f"{c.get('Name', 'Not Found')} ({d}) Done")
        index = len(champlist)
        champlist.append(c)
        if len(c) > maxtuple[2]:
            maxtuple = index, d, len(c)
        if len(c) < mintuple[2]:
            mintuple = index, d, len(c)

        d += 1

    # log.info(
    #     "First most keys: %s (%s) = %s",
    #     champlist[maxtuple[0]]["Name"],
    #     maxtuple[1],
    #     maxtuple[2],
    # )

    # log.info(
    #     "First least keys: %s (%s) = %s",
    #     champlist[mintuple[0]]["Name"],
    #     mintuple[1],
    #     mintuple[2],
    # )

    f = open("key1.txt", mode="w")
    print(champlist[maxtuple[0]]["Name"], file=f)
    # for key in sorted(champlist[maxtuple[0]].keys()):
    for key in champlist[maxtuple[0]].keys():
        print(key, file=f)
    f.close()

    f = open("key2.txt", mode="w")
    print(champlist[mintuple[0]]["Name"], file=f)
    # for key in sorted(champlist[mintuple[0]].keys()):
    for key in champlist[mintuple[0]].keys():
        print(key, file=f)
    f.close()
