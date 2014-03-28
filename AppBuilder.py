'''
Created on 28-Mar-2014

@author: Abhimanyu
'''

import os

def build(location):
    os.chdir(location)
    os.system("make")

