'''
Created on 17-Mar-2014

@author: Abhimanyu
'''

import xml.etree.ElementTree as ET
import ParserDepot

PATH_PARENT_XML = "XMLfiles/parent_app_data.xml"

class XMLParserFactory(): 
    def __init__(self, app_name, version):
        self.get_relevant_modules(app_name, version)
        
    def get_relevant_modules(self, app_name, version): 
        ''' Assigns relevant objects to class variables that hold the Parent, App and Config XML parsers.
        ''' 
        data = {}      
        tree = ET.parse(PATH_PARENT_XML)
        root = tree.getroot()
        self.parent_xml_obj= getattr(ParserDepot, "ParentXML_v_%s" % "_".join(root.attrib["version"].split(".")))(app_name, version, root)
        print "Parsing Parent XML."
        parent_xml_data = self.parent_xml_obj.parse()
        
        self.app_xml_obj = getattr(ParserDepot, "AppXML_v_%s" % "_".join(parent_xml_data["app_xml_version"].split(".")))(parent_xml_data["app_xml_location"])
        print "Parsing %s." % (parent_xml_data["app_xml_location"])
        app_xml_data = self.app_xml_obj.parse()
        
        self.cfg_xml_obj = getattr(ParserDepot, "CfgXML_v_%s" % "_".join(parent_xml_data["cfg_xml_version"].split(".")))(parent_xml_data["cfg_xml_location"])
        print "Parsing %s." % (parent_xml_data["cfg_xml_location"])
        cfg_xml_data = self.cfg_xml_obj.parse()
        
        data["parent_xml_data"] = parent_xml_data
        data["app_xml_data"] = app_xml_data
        data["cfg_xml_data"] = cfg_xml_data
        
        self.data = data
    
    def get_data(self):
        return self.data
        
def get_info(app_name, version):
    ''' Drives the XML parsing process to extract complete information about the app and returns the data to parent.
    '''
    xml_parse_obj = XMLParserFactory(app_name, version)
    data = xml_parse_obj.get_data()
    
    return data

