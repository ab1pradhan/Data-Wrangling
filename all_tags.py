"""

Here iterative parsing is used to process the map file and to 
find out not only what tags are there, but also how many, to get the 
feeling on how much of which data you can expect to have in the map.It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.


'
"""


import xml.etree.cElementTree as ET

import pprint

from collections import defaultdict

OSM_FILE='Jaipurmap.osm'

def count_tags(filename):
    d = defaultdict(int)
    for _,element in ET.iterparse(filename):
    	d[element.tag]+=1
    return d   


def test():
    tags = count_tags(OSM_FILE)
    pprint.pprint(tags)


if __name__ == "__main__":
    
    test()