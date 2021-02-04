from requests_html import AsyncHTMLSession

from aycsv import save2csv
from get_champ import get_champ
from getlinks import getlinks


def addarg(tierLink):
    async def wrapper():
        resp = await asession.get(tierLink[0])
        champlist.append(get_champ(resp, tierLink))
        return resp

    return wrapper


def getfuncgen(tuplist, size):
    def gettupgen(tl):
        for t in tl:
            yield t

    tups = gettupgen(tuplist)

    while True:
        ts = []
        for _ in range(size):
            try:
                ts.append(addarg(next(tups)))
            except StopIteration:
                break
        if not ts:
            break
        yield ts


# Use parent page to get a list of dictioaries with 'tier' and 'url' as keys
tierLinkList = getlinks()
# Instanciate list for champion dictionaries
champlist = []
# Generate list of funtion pointers in groups of 12
funclists = getfuncgen(tierLinkList, 12)
# open async session
asession = AsyncHTMLSession()
for funclist in funclists:
    # Run all functions in list
    asession.run(*funclist)

save2csv(champlist, "champs.csv")
