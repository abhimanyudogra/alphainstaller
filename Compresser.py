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
        binary_files = XMLInfoExtracter.get_binary_paths(xml_files_data["bin_xml_location"], xml_files_data["bin_xml_version"])
        config_files = XMLInfoExtracter.get_config_file_paths(xml_files_data["cfg_xml_location"], xml_files_data["cfg_xml_version"])
        scr_files = XMLInfoExtracter.get_scr_paths(xml_files_data["scr_xml_location"], xml_files_data["scr_xml_version"])
        self.comp_obj.compress(binary_files, config_files, scr_files)


class Compresser_targz():
    def compress(self, binary_files, config_files, scr_files):
        tar = tarfile.open("alphainstaller.tar.gz", "w:gz")

        for _binary in binary_files["bin_data"]:
            tar.add(_binary["code_base_location"])

        for _file in config_files["config_data"]:
            tar.add(_file["code_base_location"])

        for scr in scr_files["script_data"]:
            tar.add(scr["code_base_location"])

        tar.close()

        