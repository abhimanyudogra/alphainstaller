'''
Created on 17-Mar-2014

@author: Abhimanyu
'''

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
        self.parser_obj = getattr(ParserDepot, "BinXMLParser_v_%s" % "_".join(version.split(".")))(location)

    def parse(self):
        return self.parser_obj.parse()


class CfgXMLParserFactory():
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "CfgXMLParser_v_%s" % "_".join(version.split(".")))(location)

    def parse(self):
        return self.parser_obj.parse()


class ScrXMLParserFactory():
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "ScrXMLParser_v_%s" % "_".join(version.split(".")))(location)

    def parse(self):
        return self.parser_obj.parse()


class TgtXMLParserFactory():
    def __init__(self, location, version):
        self.parser_obj = getattr(ParserDepot, "TgtXMLParser_v_%s" % "_".join(version.split(".")))(location)

    def parse(self):
        return self.parser_obj.parse()


def get_binary_paths(location, version):
    parser_obj = BinXMLParserFactory(location, version)
    return parser_obj.parse()


def get_config_file_paths(location, version):
    parser_obj = CfgXMLParserFactory(location, version)
    return parser_obj.parse()


def get_scr_paths(location, version):
    parser_obj = ScrXMLParserFactory(location, version)
    return parser_obj.parse()
