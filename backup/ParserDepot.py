'''
Created on 28-Mar-2014

@author: Abhimanyu
'''
from abc import ABCMeta, abstractmethod
import xml.etree.ElementTree as ET

class XMLParser():
    ''' Abstract Base class for all parsing modules
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def parse(self):
        pass
    
class ParentXMLParser(XMLParser):
    ''' Abstract Base class for all Parent XML parsing modules
    '''
    __metaclass__ = ABCMeta
    def __init__(self, app_name, version, root):
        XMLParser.__init__(self)
        self.app_name = app_name
        self.version = version
        self.root = root
        
    
class ParentXML_v_0_0(ParentXMLParser):
    ''' Parsing module for v0.0 of Parent XML
    '''
    def __init__(self, location, app_name, version):
        ParentXMLParser.__init__(self, location, app_name, version)
        
    def parse(self):                
        parent_xml_data = {}          
        tree = ET.parse(self.location)
        root = tree.getroot()
                
        for app in root:
            if app.attrib["name"] == self.app_name:               
                for app_version in app:     #Checking the "version" node for the required version
                    if app_version.attrib["tag"] == self.version:                    
                        for info in app_version:  #Extracting all information about the relevant version of the app  
                            parent_xml_data[info.tag] = info.text            
            
        return parent_xml_data
         
     

class AppXMLParser(XMLParser):
    ''' Abstract Base Class for parsing App's sub XML files. 
    '''
    __metaclass__ = ABCMeta
    def __init__(self, location):
        XMLParser.__init__(self)
        self.location = location
    
class BinXMLParser_v_0_1(AppXMLParser):
    ''' Parsing module for v2.1 of App XML.
    '''
    def __init__(self, location):
        AppXMLParser.__init__(self, location) 
        
    def parse(self):
        bin_xml_data = {}          
        tree = ET.parse(self.location)
        root = tree.getroot()
        bin_xml_data[root.tag] = [] 
        for bin_file in root:
            data = {}
            for info in bin_file:
                data[info.tag] = info.text
            bin_xml_data[root.tag].append(data)
                    
        return bin_xml_data
    
        
class CfgXMLParser_v_0_1(AppXMLParser):
    def __init__(self, location):
        AppXMLParser.__init__(self, location)
        
    def parse(self):
        cfg_xml_data = {}          
        tree = ET.parse(self.location)
        root = tree.getroot()
        cfg_xml_data[root.tag] = [] 
        for config_file in root:
            data = {}
            for info in config_file:
                data[info.tag] = info.text
            cfg_xml_data[root.tag].append(data)
        
        return cfg_xml_data
        
        
class TgtXMLParser_v_0_1(AppXMLParser):
    def __init__(self, location):
        AppXMLParser.__init__(self, location)
        
    def parse(self):
        tgt_xml_data = {}           
        tree = ET.parse(self.location)
        root = tree.getroot()
        tgt_xml_data[root.tag] = []
        for target_machine in root:
            data = {}
            for info in target_machine:
                data[info.tag] = info.text
            tgt_xml_data[root.tag].append(data)
            
        return tgt_xml_data

class ScrXMLParser_v_0_1(AppXMLParser):
    def __init__(self, location):
        AppXMLParser.__init__(self, location)
        
    def parse(self):
        scr_xml_data = {}           
        tree = ET.parse(self.location)
        root = tree.getroot()
        scr_xml_data[root.tag] = []
        for script_file in root:
            data = {}
            for info in script_file:
                data[info.tag] = info.text
            scr_xml_data[root.tag].append(data)
        
        return scr_xml_data
      
