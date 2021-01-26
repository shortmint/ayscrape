from os import abort

from requests_html import HTMLSession


class Htmlstack:
    def __init__(self, linklist):
        self.stack = linklist
        self.index = 0
        self.eol = False

    def peek(self, delta=0):
        try:
            return self.stack[self.index + delta]
        except:
            self.eol = True
            pass

    def pop(self, delta=0):
        item = self.peek(delta)
        if item:
            self.index += 1
        return item


def star2num(str):
    return (
        str.replace("★★★★★", "5")
        .replace("★★★★✰", "4")
        .replace("★★★✰✰", "3")
        .replace("★★✰✰✰", "2")
        .replace("★✰✰✰✰", "1")
        .replace("✰✰✰✰✰", "0")
        .replace("★", "")
        .replace("✰", "")
    )


def equip_priority(e, removefirst=0):
    es = e.split("\n")[removefirst:]
    if len(es) > 3:
        del es[1:4]
    return "\n".join(es)


def search(childlist, str):
    while childlist.peek():
        if str in childlist.peek().text:
            return True
        else:
            childlist.pop()
    return False


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
    x = 0
    for dl in dlist:
        x += len(dl["links"])
    print(len(dlist), " Tier/Rarity", x, "Champions")

    d = 0  ####<<<<<<<<<<<<<<<<<<<<<<<<<####
    champlist = []
    for tier_linkDict in dlist[d : d + 1]:

        links = tier_linkDict["links"]
        u = 3  ####<<<<<<<<<<<<<<<<<<<<<####
        for url in links[u:]:
            # errorList = []
            champdict = {}
            with session.get(url) as r:
                header = r.html.find("#content header", first=True).text.split("|")
                champdict["Name"] = header[0].strip()
                print(champdict["Name"])
                print(d)
                print(u)
                champdict["Desc"] = header[1].strip()
                champdict["Tier"] = tier_linkDict["tier"][0]
                # champdict["Rarity"] = (
                #     tier_linkDict["tier"].split("|")[1].strip().split()[0]
                # )

                htmlChildList = Htmlstack(r.html.find(".entry-content > *"))

                try:
                    champdict["avatar"] = (
                        htmlChildList.pop().find("img", first=True).attrs["src"]
                    )
                    paras = Htmlstack(htmlChildList.pop().find("td p"))
                    champdict["obtain"] = paras.pop().text
                    champdict["overview"] = paras.pop().text
                    champdict["totalstats"] = paras.pop().text
                    champdict["grinding"] = star2num(paras.pop().text)
                    champdict["dungeons"] = star2num(paras.pop().text)
                    champdict["potion"] = star2num(paras.pop().text)
                    champdict["doomtower"] = star2num(paras.pop().text)
                except AttributeError:
                    pass
                # Skills
                if search(htmlChildList, champdict["Name"]):
                    htmlChildList.pop()

                    # if "Skills" in htmlChildList.pop().text:
                    skillList = []
                    while htmlChildList.peek():
                        if htmlChildList.peek().find("strong"):
                            skillList.append(htmlChildList.pop().text)
                        else:
                            break
                    champdict["skills"] = "\n".join(skillList)

                if search(htmlChildList, "Equipment"):
                    htmlChildList.pop()
                    keys = ["setArena", "setBoss", "statArena", "statBoss"]
                    table = htmlChildList.peek().find("tr p")
                    # one_p = htmlChildList.peek().find("p strong")
                    if table:
                        htmlChildList.pop()
                        for key, ele in zip(keys, table):
                            champdict[key] = ele.text

                        # champdict["setArena"] = table.pop(0).text
                        # champdict["setBoss"] = table.pop(0).text
                        # champdict["statArena"] = equip_priority(table.pop(0).text)
                        # champdict["statBoss"] = equip_priority(table.pop(0).text)
                    elif htmlChildList.peek().find("p strong"):
                        try:
                            for key in keys[:3]:
                                champdict[key] = equip_priority(
                                    htmlChildList.pop().text, removefirst=1
                                )
                            # champdict["setArena"] = equip_priority(
                            #     htmlChildList.pop().text, removefirst=1
                            # )
                            # champdict["setBoss"] = equip_priority(
                            #     htmlChildList.pop().text, removefirst=1
                            # )
                            # champdict["statArena"] = equip_priority(
                            #     htmlChildList.pop().text, removefirst=1
                            # )
                            champdict[keys[3]] = champdict["statArena"]
                        except:
                            pass
                if search(htmlChildList, "Mastery"):
                    htmlChildList.pop()

                    # while not "Mastery Guide" in htmlChildList.peek().text:
                    #     htmlChildList.pop()
                    # htmlChildList.pop()

                    areaList = [
                        "Arena",
                        "Clan",
                        "Campaign",
                        "Dungeons",
                        "Faction",
                        "Doom",
                    ]

                    mast_index = 1
                    while htmlChildList.peek():
                        if any(
                            ele in htmlChildList.peek().text for ele in areaList
                        ) or htmlChildList.peek().find("img, p"):

                            area = htmlChildList.pop().text
                            if not area:
                                area = "All"

                            while htmlChildList.peek().find("img, p"):
                                htmlChildList.pop(0)  # discard img

                            mastList = htmlChildList.pop().find("td ol, td ul")
                            if len(mastList) == 3:
                                champdict.update(
                                    [
                                        (f"area-{mast_index}", area),
                                        (f"offence-{mast_index}", mastList[0].text),
                                        (f"defence-{mast_index}", mastList[1].text),
                                        (f"support-{mast_index}", mastList[2].text),
                                    ]
                                )

                                mast_index += 1
                        else:
                            break

                print(champdict)
                print()
            u += 1
            # End of: with session.get(url) as r
        # End of: links
        d += 1
    # End of: for tier_linkDict in dlist
print("Done")
