# Counting and getting a feel for attributes of "tag" tags.



import xml.etree.cElementTree as ET

import pprint

from collections import defaultdict

OSM_FILE='sample.osm'    # using small portion of the original osm file

def count_childtags(filename):
    d=defaultdict(set)
    for _,elem in ET.iterparse(filename):
        for item in elem.iter('tag'):
            d[item.attrib['k']].add(item.attrib['v']
    return d

def test():
    tags = count_childtags(OSM_FILE)
    pprint.pprint(tags)


if __name__ == "__main__":
    
    test()