from get_champ import get_champ
from requests_html import HTMLSession

from classes import *
from functions import *
from getlinks import getlinks

import logging as log

log.basicConfig(level=log.INFO)

# log.basicConfig(
#     level=log.DEBUG, filename="root.log", format="%(asctime)%:%(levelname)%:%(message)%"
# )

# Use parent page to get the links by Champ, tier, link
dlist = getlinks()

# open session
with HTMLSession() as session:

    d = 2  # select tier start section <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # Store champion data in champlist of dictionaries
    champlist = []
    # Loop through dictionary list of links
    for tier_linkDict in dlist[d : d + 1]:  ### Tempory tier range

        links = tier_linkDict["links"]
        # Tempory logging
        u = 0  # select champion start section  <<<<<<<<<<<<<<<<<<<<<
        for url in links[-4:]:  ############### Tempory champion range
            # Get response
            with session.get(url) as r:
                champlist.append(get_champ(r, tier_linkDict))
            u += 1
            c = champlist[-1]
            log.info(f'Name: {c.get("Name", "Not Found")}')
        d += 1

        # log.debug("tomes", c.get("tomes", "Not Found"))
        # log.debug("SPD", c.get("SPD", "Not Found"))
        # log.debug("area-1", c.get("area-1", "Not Found"))
        # log.debug(len(c), ": ", d, "/", u)
