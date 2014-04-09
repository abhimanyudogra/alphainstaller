'''
Created on 31-Mar-2014

@author: Abhimanyu
'''
import tarfile

class Compress():
    def __init__(self, bin_location, other_files ):
        self.bin_location = bin_location
        self.other_files = other_files
        
    def compress(self):
        tar = tarfile.open("alphainstaller.tar.gz", "w:gz")
        tar.add(self.bin_location, arcname="%s" %self.bin_location.split("/")[-1] )
        for _file in self.other_files:
            tar.add(_file, arcname="%s" %_file.split("/")[-1])
        tar.close()