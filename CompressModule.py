'''
Created on 31-Mar-2014

@author: Abhimanyu
'''
import tarfile
import os

class Compress():
    def __init__(self, bin_location, other_files ):
        self.bin_location = bin_location
        self.other_files = other_files
        
    def compress(self):
        tar = tarfile.open("alphainstaller.tar.gz", "w:gz")
        tar.add(self.bin_location)
        for _file in self.other_files:
            tar.add(_file)
        tar.close()