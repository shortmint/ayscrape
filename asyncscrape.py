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


# Temporary function - Delete Temporaries when stable and info gleaned
def tmp_info(maxtuple, mintuple):
    clen = len(champlist)
    if len(cdir) > maxtuple[2]:
        maxtuple = clen - 1, d, len(cdir)
    if len(cdir) < mintuple[2]:
        mintuple = clen - 1, d, len(cdir)
    return maxtuple, mintuple


# level=log.DEBUG, filename="root.log", format="%(asctime)%:%(levelname)%:%(message)%"
# Configure logger
log.basicConfig(level=log.INFO, format="%(levelname)s:%(module)s:%(message)s)")


# Temporary for min/max number of dictionary items sraped: Initialise vars
maxtuple = (0, 0, 0)
mintuple = (0, 0, 10000)

# Number of async functions
chunk = 5

# Use parent page to get a list of dictioaries with 'tier' and 'url' as keys
tl = getlinks()

# Temporary: tl selects chunk from getlinks() for later processing
d = 132
# Change to tierLinkList = getlinks() when Temporary is taken out
tierLinkList = tl[d:137]

# Put end on a x*chunk boundary for async functions
end = int(len(tierLinkList) / chunk) * chunk

# Instanciate list for champion dictionaries
champlist = []
# Initialise dictionary list index
index = 0
# open async session
asession = AsyncHTMLSession()
while index < end:
    # Initialise secondary function parameters (Number of functions = chunk)
    get_resp1 = getfunc1(tierLinkList[index + 0]["url"])
    get_resp2 = getfunc2(tierLinkList[index + 1]["url"])
    get_resp3 = getfunc3(tierLinkList[index + 2]["url"])
    get_resp4 = getfunc4(tierLinkList[index + 3]["url"])
    get_resp5 = getfunc5(tierLinkList[index + 4]["url"])

    # Start async secondary functions
    resps = asession.run(get_resp1, get_resp2, get_resp3, get_resp4, get_resp5)

    # Process responses
    for i, r in enumerate(resps):
        cdir = get_champ(r, tierLinkList[index + i])
        champlist.append(cdir)
        log.info(f"{cdir.get('Name', 'Not Found')} ({d}) Done")

        # Temporary supplement information to create csv from largest dict items
        #   and smallest dict items to investigate any parsing errors
        maxtuple, mintuple = tmp_info(maxtuple, mintuple)
        d += 1
        # End of Temporary info

    index += chunk
rem = len(tierLinkList) % chunk
# Deal with stragglers
session = HTMLSession()
while rem:
    r = session.get(tierLinkList[index]["url"])
    cdir = get_champ(r, tierLinkList[index])
    champlist.append(cdir)
    log.info(f"{cdir.get('Name', 'Not Found')} ({d}) Done")

    # Temporary supplement information to create csv from largest dict items
    #   and smallest dict items to investigate any parsing errors
    maxtuple, mintuple = tmp_info(maxtuple, mintuple)

    # clen = len(champlist)
    # if len(cdir) > maxtuple[2]:
    #     maxtuple = clen - 1, d, len(cdir)
    # if len(cdir) < mintuple[2]:
    #     mintuple = clen - 1, d, len(cdir)
    d += 1
    # End of Temporary info

    rem -= 1
    index += 1
session.close()

# Temporary min/max info
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
# End of Temporary min/max info
