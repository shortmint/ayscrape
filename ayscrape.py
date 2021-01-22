from requests_html import HTMLSession

with HTMLSession() as session:
    # Use parent page to get the links by Champ, tier, link
    with session.get(
        "https://ayumilove.net/raid-shadow-legends-list-of-champions-by-ranking/"
    ) as resp_links:
        sel = ".entry-content > h4, .entry-content > h3, .entry-content > h2, .entry-content li a"  # li... :first-child
        ranks = resp_links.html.find(sel)

        dlist = []
        linklist = []
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

    d = 1  ######<<<<<<<<<<<<<<<<<<<<<<<######
    for tier_linkDict in dlist[d : d + 1]:
        tier = tier_linkDict["tier"]
        links = tier_linkDict["links"]
        u = 0  ######<<<<<<<<<<<<<<<<<<#######
        for url in links[u:]:
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
                        f'{d}->{u}\t{len(mlist)}: {mlist[0]["area"], mlist[0]["offence"][:16]})'
                    )
                if errorList:
                    print(errorList[0])
                print()
                # End of: if "Mastery Guide"
            # End of: with session.get(url) as r
        u += 1
        # End of: links
    d += 1
    # End of: for tier_linkDict in dlist
