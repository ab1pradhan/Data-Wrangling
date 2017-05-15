# finding out how many unique users 
have contributed to the map in this area!

import xml.etree.cElementTree as ET

import pprint

import re

OSM_FILE='Jaipurmap.osm'

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == 'node':
            users.add(element.attrib['uid'])

    return users


def test()
    users = process_map(OSM_FILE)
    pprint.pprint(users)


if __name__ == "__main__":

    test()