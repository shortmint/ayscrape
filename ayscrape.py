from requests_html import HTMLSession


class Htmlstack:
    def __init__(self, linklist):
        self.stack = linklist
        self.index = 0

    def peek(self, delta=0):
        try:
            return self.stack[self.index + delta]
        except:
            return None

    def pop(self):
        item = self.peek()
        if item:
            self.index += 1
        return item


with HTMLSession() as session:
    # Use parent page to get the links by Champ, tier, link
    with session.get(
        "https://ayumilove.net/raid-shadow-legends-list-of-champions-by-ranking/"
    ) as resp_links:
        sel = ".entry-content > h4, .entry-content > h3, .entry-content > h2, .entry-content li a"  # li... :first-child
        ranks = resp_links.html.find(sel)

        dlist = []
        linklist = []
        # Fetch first element for loop
        tier = ranks[0].text
        for rank in ranks[1:]:
            link = rank.find("a", first=True)
            if not link:
                if linklist:
                    dlist.append({"tier": tier, "links": linklist})
                    linklist = []
                tier = rank.text
            else:
                linklist.append(link.attrs["href"])
    print(len(dlist))
    x = 0
    for dl in dlist:
        x += len(dl["links"])
    print(x)

    d = 6  ####<<<<<<<<<<<<<<<<<<<<<<<<<####
    for tier_linkDict in dlist[d : d + 1]:
        tier = tier_linkDict["tier"]
        links = tier_linkDict["links"]
        u = 25  ####<<<<<<<<<<<<<<<<<<<<<####
        for url in links[u : u + 1]:
            errorList = []
            with session.get(url) as r:
                sel = ".entry-content > *"
                htmlChildList = r.html.find(sel)

                htmlChildElement = htmlChildList.pop(0)
                jpeg = htmlChildElement.find("img", first=True).attrs["src"]
                print("jpeg: ", jpeg)

                htmlChildElement = htmlChildList.pop(0)
                paras = htmlChildElement.find("td p")
                obtain = paras.pop(0).text
                overview = paras.pop(0).text
                totalstats = paras.pop(0).text
                grinding = paras.pop(0).text
                dungeons = paras.pop(0).text
                potion = paras.pop(0).text
                doomtower = paras.pop(0).text

                if "Skills" in htmlChildList.pop(0).text:
                    # skill = htmlChildList.pop(0)
                    skillList = []
                    while htmlChildList[0].find("strong"):
                        skillList.append(htmlChildList.pop(0).text)

                if "Equipment Guide" in htmlChildList.pop(0).text:
                    elems = htmlChildList[0].find("tr p")
                    if elems:
                        setArena = elems.pop(0).text
                        setBoss = elems.pop(0).text
                        statArena = elems.pop(0).text
                        statBoss = elems.pop(0).text
                    else:
                        while not "Mastery Guide" in htmlChildList[0].text:
                            errorList.append({"equip": htmlChildList[0].html})
                            htmlChildList.pop(0)

                if "Mastery Guide" in htmlChildList.pop(0).text:
                    areaList = [
                        "Arena",
                        "Clan",
                        "Campaign",
                        "Dungeons",
                        "Faction",
                        "Doom",
                    ]

                    mlist = []
                    while any(
                        ele in htmlChildList[0].text for ele in areaList
                    ) or htmlChildList[0].find("img, p"):

                        area = htmlChildList.pop(0).text
                        # Assume i
                        if not area:
                            area = "All"
                        while htmlChildList[0].find("img, p"):
                            htmlChildList.pop(0)  # discard img
                        mastList = htmlChildList.pop(0).find("td ol, td ul")
                        if len(mastList) == 3:
                            mlist.append(
                                {
                                    "area": area,
                                    "offence": mastList[0].text,
                                    "defence": mastList[1].text,
                                    "support": mastList[2].text,
                                }
                            )

                    print(
                        f'{d:3}->{u:2}, {len(mlist)}: {mlist[0]["area"], mlist[0]["offence"]}'
                    )
                if errorList:
                    print(errorList[0])
                print()
                # End of: if "Mastery Guide"
            u += 1
            # End of: with session.get(url) as r
        # End of: links
    d += 1
    # End of: for tier_linkDict in dlist
print("Done")
