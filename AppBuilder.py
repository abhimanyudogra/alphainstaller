'''
Created on 28-Mar-2014

@author: Abhimanyu
'''

import os
from abc import ABCMeta, abstractmethod

from utilities import FatalError


class BuildFactory():
    '''
    Factory module that selects relevant builder module based on settings XML.
    '''
    def __init__(self, location, _type):
        if os.path.exists(location):
            if _type == "make":
                self.build_tool_obj = MakeBuilder(location)
        else:
            raise FatalError("Cannot find build automation file at: %s" % location)

    def build(self):
        self.build_tool_obj.build()


class Builder(object):
    ''' 
    Abstract base class for all builder modules.
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def build(self):
        pass


class MakeBuilder(Builder):
    ''' 
    Module that builds the code-base using Make utility.
    '''
    def __init__(self, target):
        Builder.__init__(self)
        self.target = target

    def build(self):
        print "Invoking make-file:  %s " % self.target
        os.system("make -f Makefile")