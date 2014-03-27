'''
Created on 27-Mar-2014

@author: Abhimanyu
'''


import os  
from abc import ABCMeta, abstractmethod


class CheckoutFactory(object): 
    __metaclass__ = ABCMeta   
    def __init__(self, repo_type, source, target):
        self.source = source
        self.target = target  
        self.CheckoutSubType = self.get_relevant_checkout()
        
    def get_relevant_checkout(self):
        if self.repo_type == "svn":
            return SVNCheckout(self.source, self.target)   

    def checkout_code(self):
        return self.CheckoutSubType.checkout_code()        
          
        
class SVNCheckout():    
    def __init__(self, source, target):
        self.source = source
        self.target = target
        
    def checkout_code(self):
        print "Checking out data from repository."
        os.system("svn checkout file://%s %s"%(self.source, self.target))
        
class GitCheckout():
    def __init__(self, source, target):
        self.source = source
        self.target = target
        
    def checkout_code(self):
        pass
        

