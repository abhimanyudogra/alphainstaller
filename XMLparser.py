'''
Created on 17-Mar-2014

@author: Abhimanyu
'''
import os
import xml.etree.ElementTree as ET
PATH_PARENT_XML = "XMLfiles/parent_app_data.xml"
from abc import ABCMeta, abstractmethod

class XMLParser():
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def parse(self):
        pass
    
class ParentXMLParser(XMLParser):
    pass
class ConfigXMLParser():
    pass
class AppXMLParser():
    pass
    
def XMLDataExtracter(app_name, version):
    parser = XMLParser(app_name, version)
    









def parse(app_name, version):        
  
    def appXMLparser(target): 
        print "Parsing %s"%(target)       
        tree = ET.parse(target)
        root = tree.getroot()
        for xmldata in root:
            if xmldata.tag == "repo_type":
                repo_type = xmldata.text
            elif xmldata.tag == "repo_location":
                repo_location = xmldata.text
        
        return repo_type, repo_location
    
    def cfgXMLparser(target):
        pass
    
    def v0_0parser(app_name, version_no, root):
        print "Parsing %s."%(PATH_PARENT_XML)
        app_data = {}
        target_machines = []
        config_xml_address = ""
        app_xml_address = ""
        
        for data in root:
            if data.tag == "app":
                if data.attrib["name"] == app_name:                 
                    for version in data:                    
                        if version.attrib["tag"] == version_no:                    
                            for info in version:
                                if info.tag == "target":                                
                                    target_machines.append(info.attrib["ip"])                            
                                elif info.tag == "%s_v%s_cfg" %(app_name, version_no):                                
                                    config_xml_address = info.attrib["address"]
                                elif info.tag == "%s_v%s" %(app_name, version_no):
                                    app_xml_address = info.attrib["address"]
            if data.tag == "temp_folder":
                app_data["temp_folder_address"] = data.attrib["address"]
                                    
        repo_type, repo_location = appXMLparser(app_xml_address)
        
        app_data["name"] = app_name
        app_data["version"] = version_no
        app_data["repo_type"] = repo_type
        app_data["repo_location"] = repo_location
        
        return app_data
    
        
        #cfgXMLparser(config_xml_address)
                   
                      
                        
  
    tree = ET.parse(PATH_PARENT_XML)
    root = tree.getroot()    
    return locals()["v%sparser" % "_".join(root.attrib['version'].split("."))](app_name, version, root) # Calls the respective function for parsing the given version of XML
    
if __name__ == "__main__":
    print "parsing app1"
    parse("app1", "1.01")
    print "parsing app1, v2.00"
    parse("app1", "2.00")
    print "parsing app2, v4.7"
    parse("app2", "4.7")
    print "parsing app3, v11.1"
    parse("app3","11.1")
     
    
