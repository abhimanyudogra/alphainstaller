'''
Created on 14-Apr-2014

@author: Abhimanyu
'''
import re
import os
from datetime import datetime

SERVER_DB = os.path.join("alphagit", os.path.join("alphadata", "server data"))
APP_DB = os.path.join("alphagit", os.path.join("alphadata", "app data"))

class Logger():
    '''
    Creates log entires for actions. Stores the username, time, checkpoints and subprocesses.
    '''
    def __init__(self, session):
        '''
        Creates the log file if it doesn't exist.
        Begins a new entry for the current action with time-stamp.
        '''
        self.checkpoint_id = 0
        self.log_location = os.path.join(APP_DB, os.path.join(session["app_name"], "v%s" % session["version"]))
        if not os.path.exists(self.log_location):
            os.makedirs(self.log_location)
        self.main_log_obj = open(os.path.join(self.log_location, "main log"), "a+")
        if self.main_log_obj.read():
            self.main_log_obj.write("\n\n\n")
        self.main_log_obj.write("[ACTION_BEGIN]>> %s : %s : %s\n" % (session["action"], session["username"], datetime.now().isoformat()))
        
        self.session = session
        
    def reset_cp(self):
        self.checkpoint_id = 0

    def add_main_log(self, description):
        '''
        Marks a subprocess in the log.
        '''
        print description
        self.main_log_obj.write("\tSUBPROCESS>> %s\n" % description)
        
    def add_remote_log(self, description):
        print description
        self.server_log_obj.write("\tSUBPROCESS>> %s\n" % description)
        
        
    def mark_local_complete(self):
        print "Local operations successfully completed. Initiating remote procedures."        
        self.main_log_obj.write("[LOCAL PROCEDURES COMPLETE]\n")
        self.reset_cp()

    def mark_local_checkpoint(self, desc):
        '''
        Marks a local checkpoint in the log.
        '''
        self.checkpoint_id += 1
        print "\nMarking local checkpoint %d ...\n" % self.checkpoint_id
        self.main_log_obj.write("[LOCAL CHECKPOINT::%d]>> %s\n" % (self.checkpoint_id, desc))

    def mark_server_end(self, ip):
        '''
        Marks the completion of operations of a specific server.
        '''
        print "Marking operations on server %s as successful." % ip
        self.server_log_obj.write("[ACTION_COMPLETE]>> %s\n" % datetime.now().isoformat())
        self.server_log_obj.close()
        
        self.main_log_obj.write("[SERVER END::%s]\n" % ip)
        self.reset_cp()
        
        
        
    def mark_server_begin(self, ip):
        '''
        '''
        print "Beginning operations on server %s. " % ip
        server_log_path = os.path.join(self.log_location, ip)
        self.server_log_obj = open(server_log_path, "a+")
        if self.server_log_obj.read():
            self.server_log_obj.write("\n\n\n")
        self.server_log_obj.write("[ACTION_BEGIN]>> %s : %s : %s\n" % (self.session["action"], self.session["username"], datetime.now().isoformat()))
        
        link_location = os.path.join(SERVER_DB, os.path.join(ip, os.path.join(self.session["app_name"], "v%0.1f" % os.path.join(self.session["version"]))))
        
        if not os.path.exists(link_location):
            os.makedirs(link_location)
        
        link_location = os.path.join(link_location, "log")
        try:
            os.symlink(server_log_path, link_location)
        except OSError:
            os.unlink(link_location)
            os.symlink(server_log_path, link_location)
         
        self.main_log_obj.write("[SERVER BEGIN::%s]\n" % ip)
        
    def mark_remote_checkpoint(self, desc):
        '''
        Marks a remote checkpoint in the log.
        '''
        self.checkpoint_id += 1
        print "\nMarking remote checkpoint %s.\n" % (self.checkpoint_id)
        self.server_log_obj.write("[REMOTE CHECKPOINT::%d]>> %s\n" % (self.checkpoint_id, desc))
        
        
    def skip_main_checkpoint(self):
        '''
        Skips a checkpoint, usually because it was successfuly reached in last action which is being resumed,
         probably due to abrupt termination of the action.
        '''
        self.checkpoint_id += 1
        print "\nSkipping checkpoint %d...\n" % self.checkpoint_id
        self.main_log_obj.write("[SKIPPED CHECKPOINT::%d]\n" % self.checkpoint_id)
        
    def skip_remote_checkpoint(self):
        self.checkpoint_id += 1
        print "\nSkipping checkpoint %d...\n" % self.checkpoint_id
        self.main_log_obj.write("[SKIPPED CHECKPOINT::%d]\n" % self.checkpoint_id)

    def action_complete(self):
        '''
        Marks the completion of the action in the log file.
        '''
        print "Action completed successfully."
        self.main_log_obj.write("[ACTION_COMPLETE]>> %s\n" % datetime.now().isoformat())
        self.main_log_obj.close()
        
        
class LogChecker():
    '''
    Log file checker module that detects abrupt termination of program and extracts last successful checkpoint.
    '''
    def __init__(self, session):
        self.location = os.path.join(APP_DB, os.path.join(session["app_name"], "v%s" % session["version"]))
        self.log_f = open(os.path.join(self.location, "main log"), "r").readlines()
        
    def get_resume_data(self):
        if not self.check_local_completion():
            return self.get_last_local_checkpoint(), {"completed_servers":[], "partially_completed_servers":[]}
        else:            
            complete , partial = self.get_deployed_servers()
            return float("inf"), {"completed_servers":complete, "partially_completed_servers":partial}


    def check_successful_completion(self):
        '''
        Checks the log file for whether the last action was successfully completed.
        '''
        i = 1
        if self.log_f:
            actcomp_re = re.compile('^\[ACTION_COMPLETE\]')
            actstrt_re = re.compile('^\[ACTION_BEGIN\]')
            while True:
                if actcomp_re.search(self.log_f[-i]):
                    return True
                if actstrt_re.search(self.log_f[-i]):
                    return False
                i += 1
        else:
            return True
    
    def check_local_completion(self):
        '''
        Checks whether the local operations were completed. Returns True if they were, False otherwise.
        '''
        i = 1
        if self.log_f:
            lcomp_re = re.compile('^\[LOCAL PROCEDURES COMPLETE\]')
            actstrt_re = re.compile('^\[ACTION_BEGIN\]')
            while True:
                if lcomp_re.search(self.log_f[-i]):
                    return True
                if actstrt_re.search(self.log_f[-i]):
                    return False
                i += 1
        else:
            return True
        
    def get_last_local_checkpoint(self):
        '''
        Extracts last successful checkpoint.
        '''
        i = 1
        chkpt_re = re.compile('^\[LOCAL CHECKPOINT::(\d+)\]') 
        actstrt_re = re.compile('^\[ACTION_BEGIN\]')
        while True:
            line = self.log_f[-i]
            latest_checkpoint = chkpt_re.findall(line)
            no_checkpoint = actstrt_re.search(line)
            if latest_checkpoint:
                return latest_checkpoint[0]
            elif no_checkpoint:
                return 0
            i += 1
        
    def get_deployed_servers(self):
        '''
        Returns two lists.
        1 - A list that contains the ip addresses of all the servers on which, the app was successfully deployed in the last session.
        2 - Second list, that contains tuple pairs of all servers, on which the app was partially deployed without completion. 
        The second component of the pair is the last successful checkpoint of that server AS INTERGER TYPE.
        '''
        i = 1
        j = 1
        completed_servers = []
        partially_completed_servers = []
        servers_already_noted = set()
        
        lcomp_re = re.compile('^\[LOCAL PROCEDURES COMPLETE\]')
        end_re = re.compile('^\[SERVER END::([\d.]+)\]')
        begin_re = re.compile('^\[SERVER BEGIN::([\d\.]+)\]')
        server_begin_re = re.compile('^\[ACTION_BEGIN\]')        
        cp_re = re.compile('^\[REMOTE CHECKPOINT::(\d+)\]')
        
        while True:
            line = self.log_f[-i]
            found_end = end_re.findall(line)
            found_begin = begin_re.findall(line)
            if found_end:
                completed_servers.append((found_end[0], 0))
            if found_begin and (found_begin[0] not in completed_servers) and (found_begin[0] not in servers_already_noted):
                server_log_location = os.path.join(self.location, found_begin[0])
                server_log_f = open(server_log_location, "a+").readlines()
                checkpoint_no = 0
                
                while True:
                    line = server_log_f[-j]
                    last_cp = cp_re.findall(line)
                    reached_start = server_begin_re.findall(line)
                    if last_cp:
                        checkpoint_no = last_cp[0]
                        break
                    elif reached_start:
                        break
                    j += 1
                    
                partially_completed_servers.append(found_begin[0], int(checkpoint_no[0]))
                servers_already_noted.add(found_begin[0])
                
            elif lcomp_re.search(self.log_f[-i]):
                break
            i += 1
                
        return completed_servers, partially_completed_servers
            
            

    