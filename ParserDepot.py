'''
Created on 28-Mar-2014

@author: Abhimanyu
'''
from abc import ABCMeta, abstractmethod
import xml.etree.ElementTree as ET


class XMLParser():
    '''
    Abstract Base class for all parsing modules
    '''
    __metaclass__ = ABCMeta

    def __init__(self, location):
        self.location = location

    @abstractmethod
    def parse(self):
        pass


class ParentXMLParser(XMLParser):
    '''
    Parsing module for v0.0 of Parent XML
    '''
    def __init__(self, location):
        XMLParser.__init__(self, location)

    def parse(self):
        parent_xml_data = {}
        tree = ET.parse(self.location)
        root = tree.getroot()

        for info in root:  # Extracting all information about the relevant version of the app
            parent_xml_data[info.tag] = info.text

        return parent_xml_data


class BinXMLParser_v_0_1(XMLParser):
    '''
    Parsing module for v0.1 of app's bin XML.
    '''
    def __init__(self, location):
        XMLParser.__init__(self, location)

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


class CfgXMLParser_v_0_1(XMLParser):
    '''
    Parsing module for v0.1 of app's cfg XML
    '''
    def __init__(self, location):
        XMLParser.__init__(self, location)

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


class TgtXMLParser_v_0_1(XMLParser):
    '''
    Parsing module for v0.1 of app's tgt XML
    '''
    def __init__(self, location):
        XMLParser.__init__(self, location)

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


class ScrXMLParser_v_0_1(XMLParser):
    '''
    Parsing module for v0.1 of app's scr XML
    '''
    def __init__(self, location):
        XMLParser.__init__(self, location)

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


class AlphainstallerXMLParser(XMLParser):
    '''
    Parsing module for v0.1 of Alphainstaller's settigs module.
    '''
    def __init__(self, location):
        XMLParser.__init__(self, location)

    def parse(self):
        alphainstaller_xml_data = {}
        tree = ET.parse(self.location)
        root = tree.getroot()
        for data in root:
            alphainstaller_xml_data[data.tag] = data.text

        return alphainstaller_xml_data
    
    def get_default(self, key):
        tree = ET.parse(self.location)
        root = tree.getroot()
        for data in root:
            if data.tag == "defaults":
                for category in data:
                    for flag in category:
                        if flag.tag == key:
                            return flag.text