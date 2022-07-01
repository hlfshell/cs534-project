import xml.etree.ElementTree as ET


def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()

    for item in root.findall("vehicleTripStatistics"):
        return item.get('totalTravelTime')

    return

travel_time = parseXML("./sim/stats.xml")
print(travel_time)