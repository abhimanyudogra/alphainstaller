'''
Created on 17-Mar-2014

@author: Abhimanyu
'''

import ParserDepot
PATH_SETTINGS_XML = "XMLfiles/alphainstaller_settings.xml"


class ParentXMLParserFactory():
    '''
    Factory module for Parent XML Parsers.
    '''
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "ParentXMLParser_v_%s" % "_".join(version.split(".")))(location)

    def parse(self, session):
        return self.parser_obj.parse(session)

    def get_tag(self, tag):
        return self.parser_obj.get_tag(self, tag)


class BinXMLParserFactory():
    '''
    Factory module for Bin XML Parsers.
    '''
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "BinXMLParser_v_%s" % "_".join(version.split(".")))(location)

    def parse(self):
        return self.parser_obj.parse()


class CfgXMLParserFactory():
    '''
    Factory module for cfg XML Parsers.
    '''
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "CfgXMLParser_v_%s" % "_".join(version.split(".")))(location)

    def parse(self):
        return self.parser_obj.parse()


class ScrXMLParserFactory():
    '''
    Factory module for scr XML Parsers.
    '''
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "ScrXMLParser_v_%s" % "_".join(version.split(".")))(location)

    def parse(self):
        return self.parser_obj.parse()


class TgtXMLParserFactory():
    '''
    Factory module for tgt XML Parsers.
    '''
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "TgtXMLParser_v_%s" % "_".join(version.split(".")))(location)

    def parse(self):
        return self.parser_obj.parse()


def get_binary_paths(location, version):
    '''
    Interacts with binary xml factory class and returns the data parsed out of bin xml.
    '''
    parser_obj = BinXMLParserFactory(location, version)
    return parser_obj.parse()


def get_config_file_paths(location, version):
    '''
    Interacts with Config xml factory class and returns the data parsed out of config xml.
    '''
    parser_obj = CfgXMLParserFactory(location, version)
    return parser_obj.parse()


def get_scr_paths(location, version):
    '''
    Interacts with script xml factory class and returns the data parsed out of script xml.
    '''
    parser_obj = ScrXMLParserFactory(location, version)
    return parser_obj.parse()

def get_default(key):
    '''
    Returns the corresponding value for a sepcific default flag matching the key parameter
    '''
    settings_obj = ParserDepot.AlphainstallerXMLParser(PATH_SETTINGS_XML)
    return settings_obj.get_default(key)
    