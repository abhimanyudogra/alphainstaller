'''
Created on 14-Apr-2014

@author: Abhimanyu
'''
import os
from datetime import datetime


class Logger():
    def __init__(self, app_name, version, action, user):
        self.checkpoint_id = 0
        
        log_location = os.path.join("Logs", os.path.join(app_name, "v%s"%version))
        if not os.path.exists(log_location):
            os.makedirs(log_location)
        self.file_obj = open(os.path.join(log_location, "log"), "a+")
        if self.file_obj.read():
            self.file_obj.write("\n\n\n")
        self.file_obj.write("[ACTION_BEGIN]>> %s : %s : %s\n" % (action, user, datetime.now().isoformat()))   
        
         
    def add_log(self, description):
        print description
        self.file_obj.write("\tSUBPROCESS>> %s\n" % description)
        
    def mark_checkpoint(self, desc):
        self.checkpoint_id+=1
        print "[MARKING CHECKPOINT]\n"
        self.file_obj.write("[CHECKPOINT::%d]>> %s\n" %(self.checkpoint_id, desc))
        
    def skip_checkpoint(self):
        self.checkpoint_id+=1
        print "Skipping checkpoint %d" %self.checkpoint_id
               
    def action_complete(self):
        print "Action completed successfully."
        self.file_obj.write("[ACTION_COMPLETE]>> %s\n" %datetime.now().isoformat())
        self.file_obj.close()
        
    
        
    