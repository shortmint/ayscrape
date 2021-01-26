from requests_html import HTMLSession


def getlinks():
    with HTMLSession() as session:
        # Use parent page to get the links by Champ, tier, link
        with session.get(
            "https://ayumilove.net/raid-shadow-legends-list-of-champions-by-ranking/"
        ) as resp_links:
            # All relevent links are in anchors <a> of lists <li> and contains a href attribute
            sel = ".entry-content > h4, .entry-content > h3, .entry-content > h2, .entry-content li a"
            champs = resp_links.html.find(sel)
            # Initialise list for dictionaries
            champLinkList = []
            # Initialise list for links
            linklist = []
            # Fetch first element for loop. Should be tier
            tier = champs[0].text[0]  # eg. 'S Rank | Legendary Champion'.  --> 'S'
            # Loop from 2nd element
            for ele in champs[1:]:
                # If it's a link...
                link = ele.find("a", first=True)
                if link:
                    # ... then build link list...
                    linklist.append(link.attrs["href"])
                else:
                    # ... else if link list exists...
                    if linklist:
                        # Create dictionary and add it to list
                        champLinkList.append({"tier": tier, "links": linklist})
                        # Empty link list
                        linklist = []
                    #  This should be next tier element. Grab the text for next dictionary
                    tier = ele.text
        return champLinkList
