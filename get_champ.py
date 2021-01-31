import logging as log
from requests_html import HTMLSession


# from functions import *
# import functions as fn
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


def test(childlist):
    try:
        if childlist[-1]:
            return True
        else:
            return False
    except IndexError:
        return False


def search(childlist, str):
    while test(childlist):
        if str in childlist[-1].text:
            return True
        else:
            childlist.pop()
    return False


def equip_priority(e):
    # Delete area data by ignoring first index
    es = e.split("\n")[1:]
    # if lines greater than 3 then delete the Weapon, Helmet and Shield (always ATK,HP and DEF)
    if len(es) >= 4:
        del es[1:4]
    return "\n".join(es)


def create_dictitems_from_list(dict, keylist, valuestr):
    vl = valuestr.split("\n")

    for k in keylist:
        for s in vl:
            if k.upper() in s:
                dict[k] = s.split(":")[-1].strip()
                break

    return


def get_champ(r, tier_linkDict):
    # Get header data
    #  Split string to list using '|' as seperater
    header = r.html.find("#content header", first=True).text.split("|")
    # Initialise champion's dictionary
    champdict = {}
    # Name is first in the list
    champdict["Name"] = header[0].strip()
    # Short description is 2nd eg.'SO-RSS' Faction-Rarity/Role/Affinity
    champdict["Desc"] = header[1].strip()
    # Get info  from passed dictionary
    champdict["Tier"] = tier_linkDict["tier"]
    champdict["Link"] = tier_linkDict["url"]
    # Get first child list of elements
    # h3 table selectors to overcome typo in html
    htmlChildList = r.html.find(
        ".entry-content > *, .entry-content h3 > table, .entry-content h3 > h3"
    )
    htmlChildList.reverse()
    # First seection is quite stable but skip collection if AttriuteError occurs
    #  or avatar is not there
    if test(htmlChildList):
        champdict["avatar"] = htmlChildList.pop().find("img", first=True).attrs["src"]
        paras = htmlChildList.pop().find("td p")
        paras.reverse()
        # keys from table
        champdict["obtain"] = paras.pop().text
        # Skip over possible elements to Overview (contains 'FACTON')
        search(paras, "FACTION")
        # overview and totalstats add keys to dictionary
        keylist = ["faction", "rarity", "role", "affinity", "usability", "tomes"]
        create_dictitems_from_list(champdict, keylist, paras.pop().text)
        # overview(champdict, paras.pop().text)
        keylist = ["HP", "ATK", "DEF", "SPD", "C.RATE", "C.DMG", "RESIST", "ACC"]
        create_dictitems_from_list(champdict, keylist, paras.pop().text)
        # totalstats(champdict, paras.pop().text)
        champdict["grinding"] = star2num(paras.pop().text)
        champdict["dungeons"] = star2num(paras.pop().text)
        champdict["potion"] = star2num(paras.pop().text)
        champdict["doomtower"] = star2num(paras.pop().text)

    # Get Equipment:
    #   Sometimes 'Equipment' is not in a heading, so use name
    if search(htmlChildList, champdict["Name"]):
        # Found heading: throw it away
        htmlChildList.pop()
        attack = 1
        # skillList = []
        # Check for end of list
        while test(htmlChildList):
            # Collect all skills
            if htmlChildList[-1].find("strong"):
                champdict[f"A{attack}"] = htmlChildList.pop().text
                attack += 1
            else:
                break
        # ... and join via newlines for single string
        # champdict["skills"] = "\n".join(skillList)

    # 'Equipment' string is curently consistent
    if search(htmlChildList, "Equipment"):
        # Found heading: throw it away
        htmlChildList.pop()
        # Next section is a <table> or a series of flat first child <p>'s
        #   define key names for champion dictioary
        keys = ["setArena", "setBoss", "statArena", "statBoss"]
        #   Try to collect data by <p> if it exists
        if test(htmlChildList):
            table = htmlChildList[-1].find("tr p")
            #   If it exists then add to dictionary...
            if table:
                # table could be processed by the finally section below but this works consistently
                htmlChildList.pop()
                for key, ele in zip(keys, table):
                    champdict[key] = ele.text
            #   ...if it doesn't then try the next 3 <strong> childs
            else:
                set_priority = []
                try:
                    while test(htmlChildList):
                        if htmlChildList[-1].find("p strong"):
                            set_priority.append(htmlChildList.pop())
                        else:
                            break

                except IndexError:
                    log.exception("Handled unexpected end in Equipment scrape")
                # Gather any data found
                finally:
                    sp = len(set_priority)
                    if sp:
                        champdict[keys[0]] = set_priority[0].text.split("\n")[1]
                        if sp == 2:
                            champdict[keys[2]] = equip_priority(set_priority[1].text)
                        elif sp >= 3:
                            champdict[keys[1]] = set_priority[1].text.split("\n")[1]
                            champdict[keys[2]] = equip_priority(set_priority[2].text)
                            if sp >= 4:
                                champdict[keys[3]] = equip_priority(
                                    set_priority[3].text
                                )

    # 'Mastery' string is curently consistent
    if search(htmlChildList, "Mastery"):
        # Found heading: throw it away
        htmlChildList.pop()
        #   'Key words' to check for in areas
        areaList = [
            "Arena",
            "Clan",
            "Campaign",
            "Dungeons",
            "Faction",
            "Doom",
        ]
        # Used to suffix mastery keys for offence, defence and support for different areas
        mast_index = 1

        while test(htmlChildList):
            # Check if 'Key word'  or <img>
            #   If <img> then all areas is assumed (consistent)
            if any(ele in htmlChildList[-1].text for ele in areaList) or htmlChildList[
                -1
            ].find("img, p"):
                # split to overcome typo in html (see above)
                area = htmlChildList.pop().text.split("\n")[0]
                if not area or len(area.split(",")) == 6:
                    area = "All"
                # If current child is <img> then discard
                while test(htmlChildList):
                    if htmlChildList[-1].find("img, p"):
                        htmlChildList.pop()
                    else:
                        break
                if not test(htmlChildList):
                    break
                # There's normally zero to 3 mastery configuations.
                # This should cater for all if tabulated (consitent)
                mastList = htmlChildList.pop().find("td ol, td ul")
                # Only handle sets of 3: offence, defence and support
                if len(mastList) == 3:
                    champdict.update(
                        [
                            (f"area-{mast_index}", area),
                            (f"offence-{mast_index}", mastList[0].text),
                            (f"defence-{mast_index}", mastList[1].text),
                            (f"support-{mast_index}", mastList[2].text),
                        ]
                    )
                    # Prepare for next set of keys
                    mast_index += 1

            #  No expected elements
            #   We're done
            else:
                break

    return champdict
