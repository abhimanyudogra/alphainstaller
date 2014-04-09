'''
Created on 17-Mar-2014

@author: Abhimanyu
'''

import xml.etree.ElementTree as ET
import ParserDepot

PATH_PARENT_XML = "XMLfiles/parent_app_data.xml"
PATH_ALPHAINSTALLER_XML = "XMLfiles/alphainstaller_cfg.xml"   

class ParentXMLParserFactory():
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "ParentXMLParser_v_%s" % "_".join(version.split(".")))(location)
        
    def parse(self, app_name, app_version):
        return self.parser_obj.parse(app_name, app_version)
    
    def get_tag(self, tag):
        return self.parser_obj.get_tag(self, tag)
    
class BinXMLParserFactory():
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "BinXMLParser_v_%s" % "_".join(version.split("."))) (location)
        
    def parse(self):
        return self.parser_obj.parse()
    
    
class CfgXMLParserFactory():
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "CfgXMLParser_v_%s" % "_".join(version.split("."))) (location)
        
    def parse(self):
        return self.parser_obj.parse()
    
class ScrXMLParserFactory():
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "ScrXMLParser_v_%s" % "_".join(version.split("."))) (location)
        
    def parse(self):
        return self.parser_obj.parse()

class TgtXMLParserFactory():
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "TgtXMLParser_v_%s" % "_".join(version.split("."))) (location)
        
    def parse(self):
        return self.parser_obj.parse()   


class ParserFactory(): 
    def __init__(self, app_name, version):
        self.get_relevant_modules(app_name, version)
        
    def get_relevant_modules(self, app_name, version): 
        '''Assigns relevant objects to class variables that hold the Parent, App and Config XML parsers.
        '''
        data = {}      
        tree = ET.parse(PATH_ALPHAINSTALLER_XML)
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
        


