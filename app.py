# import xml.etree.ElementTree as etree
from lxml import etree
from urllib.request import urlopen
import argparse
from pathlib import Path
import sys
from datetime import datetime

parser = argparse.ArgumentParser(description='Feed generation for rozetka from yandex_market')
group = parser.add_mutually_exclusive_group()
group.add_argument('-f', '--filename', help='file name yandex_market feed')
group.add_argument('-u', '--url', help='url yandex_market feed')
parser.add_argument('-t', '--timestamp', action='store_true', help='add timestamp to output file')
args = parser.parse_args()

xml = 'yandex_market.xml'

if args.filename:
    xml = args.filename
    file = Path(xml)
    if file.is_file() is False:
        print('ERROR: File \"' + xml + '\" not exist')
        sys.exit()
elif args.url:
    if args.url.split('.')[-1] != 'xml':
        print('WARNING: The URL is not ends with .xml\r\"' + args.url + '\"')
    xml = urlopen(args.url)
    if xml.getcode() != 200:
        print('ERROR: The URL is not valid\r\"' + args.url + '\"')
        sys.exit()
else:
    file = Path(xml)
    if file.is_file() is False:
        print('ERROR: File \"' + xml + '\" not exist')
        sys.exit()
    print('INFO: Convert default input file: \"' + xml + '\"')
tree = etree.parse(xml)
root = tree.getroot()


for offer in root.iter('offer'):
    for pickup in offer.iter('pickup'):
        offer.remove(pickup)
    for country in offer.iter('country_of_origin'):
        offer.remove(country)
    param = etree.SubElement(offer, 'param', {'name': 'Страна производитель'})
    param.text = 'Украина'
    offer.attrib.pop('group_id', None)
    offer.attrib.pop('id', None)
    for name in offer.iter('name'):
        offer.set('id', name.text.split('(')[1].split(')')[0])

timestamp = ''
if args.timestamp:
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
tree.write('rozetka{}.xml'.format(timestamp), encoding="UTF-8", xml_declaration=True)
sys.exit()


