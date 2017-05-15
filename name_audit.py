"""
Auditing name tags 
"""


import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

mapping={ 'en':'English',
         'hi':'Hindi',
         'ja':'Japanese',
         'kn':'Kannad',
         'ru':'Russian',
         'ta':'Tamil'
            }

OSM_FILE='Jaipurmap.osm'


def is_name(name):
    return 'name:' in name
    

def audit_name(filename):
    d=defaultdict(set)
    for _,item in ET.iterparse(filename):
        if item.tag == "node" or item.tag == "way":
            for child in item.iter('tag'):
                if is_name(child.attrib['k']):
                    s=child.attrib['k']
                    d[s[s.index(":")+1:]].add(child.attrib['k'])
    return d  



def update_name(name, mapping):   
    a=name[(name.index(":")+1):]     
    if a in mapping.keys():
        name = name.replace(a, mapping[a])
    return name


def test():
    name_types= audit_name(OSM_FILE)
    pprint.pprint(dict(name_types))

    for abbr ,language in name_types.iteritems():
        for name in language:
            better_name=update_name(name,mapping)
            print name," converted to : ",better_name
        

if __name__ == '__main__':
    test()








