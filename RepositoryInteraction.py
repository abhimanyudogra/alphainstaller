'''
Created on 27-Mar-2014

@author: Abhimanyu
'''


import os  
from abc import ABCMeta, abstractmethod


class CheckoutFactory(object):  
    ''' Module that automatically assigns relevant module for checking code out of repository based on the repo_type 
        extracted from App XML
    '''    
    def __init__(self, repo_type, source, target):
        self.source = source
        self.target = target
        self.repo_type = repo_type  
        self.checkout_subclass_obj = self.get_relevant_checkout()
        
    def get_relevant_checkout(self):
        '''Method that returns an object of relevant repository Checkout module.
        '''
        if self.repo_type == "svn":
            return SVNCheckout(self.source, self.target)   

    def checkout_code(self, app_name):
        '''Summonds the checkout_code method of Checkout subclass.
        '''
        return self.checkout_subclass_obj.checkout_code(app_name)       
          
class Checkout():
    ''' Abstract base class that provides an interface for modules that define code checkout procedure based on the type 
        of repository
    '''
    __metaclass__ = ABCMeta
    def __init__(self, source, target):
        self.source = source
        self.target = target
        
    @abstractmethod
    def checkout_code(self):
        pass     
       
class SVNCheckout(Checkout): 
    ''' Module that checks out code from SVN repositories
    '''   
    def __init__(self, source, target):
        Checkout.__init__(self, source, target)
        
    def checkout_code(self, app_name):
        ''' Creates a subfolder in Temp dir, named after the application being checked out and checks out the code in it.
        '''
        target_subdir = os.path.join(self.target, app_name)
        if not os.path.exists(target_subdir):
            os.mkdir(target_subdir)    
        os.system("svn checkout file://%s %s"%(self.source, target_subdir))
        
class GitCheckout(Checkout):
    def __init__(self, source, target):
        Checkout.__init__(self)
        
    def checkout_code(self):
        pass

