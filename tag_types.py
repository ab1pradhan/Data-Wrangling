"""
Checking the
"k" value for each "<tag>" and see if there are any potential problems.

Here are 3 regular expressions to check for certain patterns 
in the tags.
Tags are then classifeid in 4 categories and count of number of tags in each category is returned.
"""

import xml.etree.cElementTree as ET

import pprint

import re




#Regular expressions
lower = re.compile(r'^([a-z]|_)*$')

lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')



OSM_FILE='Jaipurmap.osm'

def key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.attrib['k']):
            keys['lower']+=1
        elif lower_colon.search(element.attrib['k']):
            keys['lower_colon']+=1
        elif problemchars.search(element.attrib['k']):
            keys['problemchars']+=1
        else:
            keys['other']+=1
        
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    keys = process_map(OSM_FILE)
    pprint.pprint(keys)


if __name__ == "__main__":

    test()