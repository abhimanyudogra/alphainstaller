'''
Created on 18-Feb-2014

@author: Abhimanyu
'''

import xml.etree.ElementTree as ET


def parse(app_name, version_no):
    alphainstaller_xml_data = {}
    tree = ET.parse("XMLfiles/alphainstaller_settings.xml")
    root = tree.getroot()        
    for data in root:
        alphainstaller_xml_data[data.tag] = data.text
    return alphainstaller_xml_data
print parse("app2", "4.7")