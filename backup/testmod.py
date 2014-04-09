'''
Created on 18-Feb-2014

@author: Abhimanyu
'''

import xml.etree.ElementTree as ET


def parse(app_name, version_no):
    parent_xml_data = {}          
    tree = ET.parse("XMLfiles/parent_app_data.xml")
    root = tree.getroot()
            
    for app in root:
        if app.attrib["name"] == app_name:               
            for version in app:     #Checking the "version" node for the required version
                if version.attrib["tag"] == version_no:                    
                    for info in version:  #Extracting all information about the relevant version of the app  
                        parent_xml_data[info.tag] = info.text            
        
    return parent_xml_data
        
print parse("app2", "4.7")