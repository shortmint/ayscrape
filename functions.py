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


def create_dictitems_from_list(dict, keylist, valuestr):
    vl = valuestr.split("\n")
    for k, s in zip(keylist, vl):
        dict[k] = s.split(":")[-1].strip()
        return


def overview(dict, valuestr):
    keylist = ["faction", "rarity", "role", "affinity", "usability", "tomes"]
    return create_dictitems_from_list(dict, keylist, valuestr)


def totalstats(dict, valuestr):
    keylist = ["HP", "ATK", "DEF", "SPD", "C.RATE", "C.DMG", "RESIST", "ACC"]
    return create_dictitems_from_list(dict, keylist, valuestr)
