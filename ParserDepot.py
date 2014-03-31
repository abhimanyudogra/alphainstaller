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
    def __init__(self, app_name, version, root):
        ParentXMLParser.__init__(self, app_name, version, root)
        
    def parse(self):        
        parent_xml_data = {}
        target_machines = []        
        
        for data in self.root:
            if data.tag == "applications":
                for app in data:       #Checking the "applications" node for the required app                            
                    if app.attrib["name"] == self.app_name:               
                        for version in app:     #Checking the "version" node for the required version
                            if version.attrib["tag"] == self.version:                    
                                for info in version:  #Extracting all information about the relevant version of the app  
                                    if info.tag == "app_xml_location":        #Location of app XML
                                        parent_xml_data["app_xml_location"] = info.text
                                        parent_xml_data["app_xml_version"] = info.attrib["version"]                                                       
                                    elif info.tag == "cfg_xml_location":       #Location of config XML                         
                                        parent_xml_data["config_xml_location"] = info.text
                                        parent_xml_data["config_xml_version"] = info.attrib["version"]
                                    
            if data.tag == "temp_folder_location":
                parent_xml_data["temp_folder_location"] = data.text  # Location of the temp folder to store the release after extraction from repository
            if data.tag == "repo_location":
                parent_xml_data["repo_location"] = data.text
                parent_xml_data["repo_type"] = data.attrib["type"] 
            if data.tag == "build_file_location":
                parent_xml_data["build_file_location"] = data.text
                parent_xml_data["build_file_type"] = data.attrib["type"]   
            
                
        parent_xml_data["target_machines"] = target_machines
        return parent_xml_data
         
     

class AppXMLParser(XMLParser):
    ''' Abstract Base Class for App XML parsing modules. 
    '''
    __metaclass__ = ABCMeta
    def __init__(self, location):
        XMLParser.__init__(self)
        self.location = location
    
class AppXML_v_2_1(AppXMLParser):
    ''' Parsing module for v2.1 of App XML.
    '''
    def __init__(self, location):
        AppXMLParser.__init__(self, location) 
        
    def parse(self):
        app_xml_data = {}
        app_xml_data["optional_files"] = []           
        tree = ET.parse(self.location)
        root = tree.getroot()
        for info in root:
            if info.tag == "binary_location":
                app_xml_data["binary_location"] = info.text
            elif info.tag == "optional_files":
                for _file in info:
                    app_xml_data["optional_files"].append(_file.text)
                    
        return app_xml_data
