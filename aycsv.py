import csv

fieldnames = [
    "Name",
    "Desc",
    "Tier",
    "Link",
    "avatar",
    "obtain",
    "faction",
    "rarity",
    "role",
    "affinity",
    "usability",
    "tomes",
    "HP",
    "ATK",
    "DEF",
    "SPD",
    "C.RATE",
    "C.DMG",
    "RESIST",
    "ACC",
    "grinding",
    "dungeons",
    "potion",
    "doomtower",
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "setArena",
    "setBoss",
    "priorityArena",
    "statArena",
    "priorityBoss",
    "statBoss",
    "area-1",
    "offence-1",
    "defence-1",
    "support-1",
    "area-2",
    "offence-2",
    "defence-2",
    "support-2",
    "area-3",
    "offence-3",
    "defence-3",
    "support-3",
    "area-4",
    "offence-4",
    "defence-4",
    "support-4",
]


def save2csv(dictlist, filename):
    with open(filename, "w", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)

        csv_writer.writeheader()

        for row in dictlist:
            csv_writer.writerow(row)
