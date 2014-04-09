'''
Created on 31-Mar-2014

@author: Abhimanyu
'''
import tarfile
import XMLInfoExtracter

class CompresserFactory():
    def __init__(self, compression_type):               
        self.comp_obj = globals()["Compresser_%s" % (compression_type)]()        
    
    def compress(self, xml_files_data):
        binary_files = self.get_binary_paths(xml_files_data["bin_xml_location"], xml_files_data["bin_xml_version"])        
        support_files = self.get_sfile_paths(xml_files_data["cfg_xml_location"], xml_files_data["cfg_xml_version"])        
        scr_files = self.get_scr_paths(xml_files_data["scr_xml_location"], xml_files_data["scr_xml_version"])
        self.comp_obj.compress(binary_files, support_files, scr_files)
        
    def get_binary_paths(self, location, version):
        parser_obj = XMLInfoExtracter.BinXMLParserFactory(location, version)
        return parser_obj.parse()
    
    def get_sfile_paths(self, location, version):
        parser_obj = XMLInfoExtracter.CfgXMLParserFactory(location, version)
        return parser_obj.parse()
    
    def get_scr_paths(self, location, version):
        parser_obj = XMLInfoExtracter.ScrXMLParserFactory(location, version)
        return parser_obj.parse()
    
        
    
    
    
    
class Compresser_targz():
        
    def compress(self, binary_files, support_files, scr_files):
        print binary_files
        print support_files
        print scr_files
        
        '''
        tar = tarfile.open("alphainstaller.tar.gz", "w:gz")
        tar.add(self.bin_location, arcname="%s" %self.bin_location.split("/")[-1] )
        for _file in self.other_files:
            tar.add(_file, arcname="%s" %_file.split("/")[-1])
        tar.close()'''
        