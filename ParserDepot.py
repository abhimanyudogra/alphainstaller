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
                                        parent_xml_data["cfg_xml_location"] = info.text
                                        parent_xml_data["cfg_xml_version"] = info.attrib["version"]
                                    
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
    
class CfgXMLParser(XMLParser):
    __metaclass__ = ABCMeta
    
    def __init__(self, location):
        XMLParser.__init__(self)
        self.location = location
        
        
class CfgXML_v_0_2(CfgXMLParser):
    def __init__(self, location):
        CfgXMLParser.__init__(self, location)
        
    def parse(self):
        cfg_xml_data = {}
        cfg_xml_data["target_machines"] = []
        target_machine_data = {}
        
        
        target_machine_data["other_files"] = []
        tree = ET.parse(self.location)
        root = tree.getroot()
        
        for info in root:
            if info.tag == "target_machine":                
                target_machine_data["os"] = info.attrib["os"]
                target_machine_data["transmit_method"] = info.attrib["transmit_method"]
                target_machine_data["ssh_username"] = info.attrib["ssh_username"]
                target_machine_data["ssh_password"] = info.attrib["ssh_password"]                
                for element in info:
                    if element.tag == "ip_address":
                        target_machine_data["ip_address"] = element.text
                    elif element.tag == "release_folder_path":
                        target_machine_data["release_folder_path"] = element.text
                    elif element.tag == "binary_file":
                        for bin_data in element:
                            if bin_data.tag == 'source_path':
                                target_machine_data["bin_source_path"] = bin_data.text
                            elif bin_data.tag == "install_path":
                                target_machine_data["bin_install_path"] = bin_data.text
                    elif element.tag == "other_files":
                        for _file in element:
                            _file_data = {}
                            for element in _file:                                
                                if element.tag == "source_path":
                                    _file_data["source_path"] = element.text
                                elif element.tag == "install_path":
                                    _file_data["install_path"] = element.text
                            target_machine_data["other_files"].append(_file_data)
                            
                cfg_xml_data["target_machines"].append(target_machine_data)        
        return cfg_xml_data    
