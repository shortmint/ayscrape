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

            # Initialise list for links
            linklist = []
            # Fetch first element for loop. eg. 'S Rank | Legendary Champion'.  --> 'S'
            tier = champs[0].text.strip()[0]
            # Loop from 2nd element
            for ele in champs[1:]:
                # If it's a link...
                link = ele.find("a", first=True)
                if link:
                    try:
                        # ... then build link list with current tier
                        linklist.append((link.attrs["href"], tier))
                    except AttributeError:
                        pass
                    except KeyError:
                        pass
                else:
                    #  This should be next tier element. Grab the first char for next tier
                    tier = ele.text.strip()[0]
        return linklist


getlinks()
