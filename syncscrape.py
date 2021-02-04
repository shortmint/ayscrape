import logging as log

from requests_html import HTMLSession

from aycsv import save2csv
from get_champ import get_champ
from getlinks import getlinks

log.basicConfig(level=log.WARNING, format="%(levelname)s:%(module)s:%(message)s)")

# level=log.DEBUG, filename="root.log", format="%(asctime)%:%(levelname)%:%(message)%"

# Use parent page to get the link by (tier, link) tuples
tierLinkList = getlinks()
tlen = len(tierLinkList)

# open session
with HTMLSession() as session:

    # Store champion data in champlist of dictionaries
    champlist = []
    # Loop through dictionary list of link
    for index, tier_link in enumerate(tierLinkList[:11]):
        with session.get(tier_link[0]) as r:
            c = get_champ(r, tier_link)

        log.info(f"{c.get('Name', 'Not Found')} ({index}) Done")
        index = len(champlist)
        champlist.append(c)
        prog = int((index * 100 + 1) / len(tierLinkList))
        p = int(prog / 10)
        print(
            f"{prog}% [{'**********'[:p+1]}]",
            end="\r",
        )
        # {'***' if index%3==2 else '** ' if index%3 else '*  '}
    # save2csv(champlist)
