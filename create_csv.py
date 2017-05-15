#Cleaning and shaping data anf then parsing it csv

  
import csv
import codecs
import re
import xml.etree.cElementTree as ET
from unittest import TestCase

import cerberus
import schema

OSM_FILE = "Jaipurmap.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

mapping={ 'af':'Afrikaans',
'alt':'Southern Altai',
'am':'Amharic',
'an':'Aragonese',
'ar':'Arabic',
'as':'Assamese',
'az':'Azerbaijani',
'be':'Belarusian',
'bg':'Bulgarian',
'bn':'Bengali',
'bo':'Tibetan',
'br':'Breton',
'bs':'Bosnian',
'ca':'Catalan',
'cs':'Czech',
'cy':'Welsh',
'da':'Danish',
'de':'German',
'dv':'Divehi',
'el':'Greek',
'en':'English',
'eo':'Esperanto',
'es':'Spanish',
'et':'Estonian',
'eu':'Basque',
'fa':'Persian',
'fi':'Finnish',
'fr':'French',
'ga':'Irish',
'gl':'Galician',
'gu':'Gujarati',
'he':'Hebrew',
'hi':'Hindi',
'hr':'Croatian',
'hu':'Hungarian',
'hy':'Armenian',
'ia':'Interlingua',
'id':'Indonesian',
'is':'Icelandic',
'it':'Italian',
'ja':'Japanese',
'jv':'Javanese',
'ka':'Georgian',
'kk':'Kazakh',
'kn':'Kannada',
'ko':'Korean',
'la':'Latin',
'lb':'Luxembourgish',
'li':'Limburgan',
'lt':'Lithuanian',
'lv':'Latvian',
'mk':'Macedonian',
'ml':'Malayalam',
'mr':'Marathi',
'ms':'Malay',
'my':'Burmese',
'ne':'Nepali',
'nl':'Dutch',
'nn':'Norwegian Nynorsk',
'no':'Norwegian',
'oc':'Occitan',
'or':'Oriya',
'pa':'Panjabi',
'pl':'Polish',
'pt':'Portuguese',
'ro':'Romanian',
'ru':'Russian',
'sa':'Sanskrit',
'sk':'Slovak',
'sl':'Slovenian',
'sr':'Serbian',
'sv':'Swedish',
'sw':'Swahili',
'ta':'Tamil',
'te':'Telugu',
'tg':'Tajik',
'th':'Thai',
'tk':'Turkmen',
'tl':'Tagalog',
'tr':'Turkish',
'uk':'Ukrainian',
'ur':'Urdu',
'vi':'Vietnamese',
'yi':'Yiddish',
'zh':'Chinese'
}

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  

    if element.tag == 'node':
        for att in NODE_FIELDS:
            node_attribs[att]=element.attrib[att]
        
        for child in element:
            node_tag = {}
            if child.attrib['k'] == 'postal_code':
                node_tag['key']='Postcode'
                node_tag['type']='Addr'
                node_tag['id']= element.attrib['id']
                node_tag['value']=child.attrib['v']
                tags.append(node_tag)
            elif LOWER_COLON.match(child.attrib['k']):
                if 'name' in child.attrib['k']:
                    part= update_name(child.attrib['k'],mapping).split(':',1)
                    node_tag['type'] =part[0].title().replace("_"," ")              #using title() to get Title from the string
                    node_tag['key'] =part[1].title().replace("_"," ")               # Replacing undescore with space
                else: 
                    node_tag['type'] = child.attrib['k'].split(':',1)[0].title().replace("_"," ")
                    node_tag['key'] = child.attrib['k'].split(':',1)[1].title().replace("_"," ")
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = child.attrib['v'].title().replace("_"," ")
                tags.append(node_tag)
            elif PROBLEMCHARS.match(child.attrib['k']):
                continue
            else:
                node_tag['type'] = 'Regular'
                node_tag['key'] = child.attrib['k'].title().replace("_"," ")
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = child.attrib['v'].title().replace("_"," ")
                tags.append(node_tag)
        
        return {'node': node_attribs, 'node_tags': tags}
        
    elif element.tag == 'way':
        for item in WAY_FIELDS:
            way_attribs[item]=element.attrib[item]
        
        
        for child in element:
            way_tag = {}
            
            if child.tag == 'tag':
                if child.attrib['k'] == 'postal_code':
                    way_tag['key']='Postcode'
                    way_tag['type']='Addr'
                    way_tag['id']= element.attrib['id']
                    way_tag['value']=child.attrib['v']
                    tags.append(way_tag)
                elif LOWER_COLON.match(child.attrib['k']):
                    if 'name' in child.attrib['k']:
                        part= update_name(child.attrib['k'],mapping).split(':',1)
                        way_tag['type'] =part[0].title().replace("_"," ")
                        way_tag['key'] =part[1].title().replace("_"," ")
                    else:   
                        way_tag['type'] = child.attrib['k'].split(':',1)[0].title().replace("_"," ")
                        way_tag['key'] = child.attrib['k'].split(':',1)[1].title().replace("_"," ")

                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v'].title().replace("_"," ")
                    tags.append(way_tag)
                elif PROBLEMCHARS.match(child.attrib['k']):
                    continue
                else:
                    way_tag['type'] = 'Regular'
                    way_tag['key'] = child.attrib['k'].title().replace("_"," ")
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v'].title().replace("_"," ")
                    tags.append(way_tag)
                    
        position = 0            
        for child in element:
            way_node = {}
            
            if child.tag == 'nd':
                way_node['id'] = element.attrib['id']
                way_node['node_id'] = child.attrib['ref']
                way_node['position'] = position
                position += 1
                way_nodes.append(way_node)
        
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def update_name(name, mapping):   
    """
	Catches abbreviations and replce thtem with full forms

         Adds the given numbers
         Args:
                   name (string): string having abbreviations
                   mapping (dictionary): maps abreviation code to full-form
         Returns:
                   name(string): Better name
    """
    a=name[(name.index(":")+1):]     
    if a in mapping.keys():
        name = name.replace(a, mapping[a])
    return name

def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    process_map(OSM_FILE, validate=False)      #Validation takes 40 times more time to process