'''
Created on 27-Mar-2014

@author: Abhimanyu
'''


import os  
from abc import ABCMeta, abstractmethod


class Checkout(object): 
    __metaclass__ = ABCMeta   
    def __init__(self, source, target):
        self.source = source
        self.target = target   
        
    @abstractmethod  
    def checkout_code(self):
        pass           
        
class SVNCheckout(Checkout):    
    def __init__(self, source, target):
        Checkout.__init__(self, source, target)
        
    def checkout_code(self):
        print "Checking out data from repository."
        os.system("svn checkout file://%s %s"%(self.source, self.target))
        
class GitCheckout(Checkout):
    def __init__(self, source, target):
        Checkout.__init__(self, source, target)
        
SVNCheckout("c","s")
GitCheckout( "d", "d")