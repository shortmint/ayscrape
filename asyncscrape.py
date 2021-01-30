import logging as log
from requests.sessions import session

from requests_html import AsyncHTMLSession, HTMLSession

from get_champ import get_champ
from getlinks import getlinks


def getfunc1(url):
    async def get_resp1():
        r = await asession.get(url)
        return r

    return get_resp1


def getfunc2(url):
    async def get_resp2():
        r = await asession.get(url)
        return r

    return get_resp2


def getfunc3(url):
    async def get_resp3():
        r = await asession.get(url)
        return r

    return get_resp3


def getfunc4(url):
    async def get_resp4():
        r = await asession.get(url)
        return r

    return get_resp4


def getfunc5(url):
    async def get_resp5():
        r = await asession.get(url)
        return r

    return get_resp5


log.basicConfig(level=log.INFO, format="%(levelname)s:%(module)s:%(message)s)")
# level=log.DEBUG, filename="root.log", format="%(asctime)%:%(levelname)%:%(message)%"

# Initialise vars for min/max length dict items
maxtuple = (0, 0, 0)
mintuple = (0, 0, 10000)
max_columns = 0
# Number of async functions
chunk = 5

# Use parent page to get the link by (tier, link) tuples
tl = getlinks()
d = 0
tierLinkList = tl[d : d + 6]

end = int(len(tierLinkList) / chunk) * chunk  #      |

# Store champion data in champlist of dictionaries
champlist = []
# Loop through dictionary list of link
index = 0
# open session
asession = AsyncHTMLSession()
while index < end:

    get_resp1 = getfunc1(tierLinkList[index + 0]["url"])
    get_resp2 = getfunc2(tierLinkList[index + 1]["url"])
    get_resp3 = getfunc3(tierLinkList[index + 2]["url"])
    get_resp4 = getfunc4(tierLinkList[index + 3]["url"])
    get_resp5 = getfunc5(tierLinkList[index + 5]["url"])

    resps = asession.run(get_resp1, get_resp2, get_resp3, get_resp4, get_resp5)
    # with session.get(tier_link["url"]) as r:
    #     cdir = get_champ(r, tier_link)
    for i, r in enumerate(resps):

        cdir = get_champ(r, tierLinkList[index + i])
        champlist.append(cdir)
        log.info(f"{cdir.get('Name', 'Not Found')} ({d}) Done")

        clen = len(champlist)
        if len(cdir) > maxtuple[2]:
            maxtuple = clen - 1, d, len(cdir)
        if len(cdir) < mintuple[2]:
            mintuple = clen - 1, d, len(cdir)
        d += 1

    index += chunk
rem = len(tierLinkList) % chunk
# Deal with stragglers
session = HTMLSession()
while rem:
    r = session.get(tierLinkList[index]["url"])
    cdir = get_champ(r, tierLinkList[index])
    champlist.append(cdir)
    log.info(f"{cdir.get('Name', 'Not Found')} ({d}) Done")

    clen = len(champlist)
    if len(cdir) > maxtuple[2]:
        maxtuple = clen - 1, d, len(cdir)
    if len(cdir) < mintuple[2]:
        mintuple = clen - 1, d, len(cdir)
    d += 1
    rem -= 1
    index += 1

# asession.close() <------ DO NOT USE
log.info(
    "First most keys: %s (%s) = %s",
    champlist[maxtuple[0]]["Name"],
    maxtuple[1],
    maxtuple[2],
)

log.info(
    "First least keys: %s (%s) = %s",
    champlist[mintuple[0]]["Name"],
    mintuple[1],
    mintuple[2],
)

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
