import xml.etree.ElementTree as ET


def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()

    for item in root.findall("vehicleTripStatistics"):
        return item.get('totalTravelTime')

    return
    for item in root.findall('./channel/item'):
        # empty news dictionary
        news = {}
        # iterate child elements of item
        for child in item:
            # special checking for namespace object content:media
            if child.tag == '{http://search.yahoo.com/mrss/}content':
                news['media'] = child.attrib['url']
            else:
                news[child.tag] = child.text.encode('utf8')

        # append news dictionary to news items list
        newsitems.append(news)

    # return news items list
    return newsitems

# with open("./sim/stats.xml", "r") as f:
#     stats = f.read()
#     parseXML(stats
travel_time = parseXML("./sim/stats.xml")
print(travel_time)