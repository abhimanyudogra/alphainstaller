'''
Created on 14-Apr-2014

@author: Abhimanyu
'''
import re
import os
from datetime import datetime


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
        log_location = os.path.join("Logs", os.path.join(session["app_name"], "v%s" % session["version"]))
        if not os.path.exists(log_location):
            os.makedirs(log_location)
        self.file_obj = open(os.path.join(log_location, "log"), "a+")
        if self.file_obj.read():
            self.file_obj.write("\n\n\n")
        self.file_obj.write("[ACTION_BEGIN]>> %s : %s : %s\n" % (session["action"], session["username"], datetime.now().isoformat()))
        
    def reset_cp(self):
        self.checkpoint_id = 0

    def add_log(self, description):
        '''
        Marks a subprocess in the log.
        '''
        print description
        self.file_obj.write("\tSUBPROCESS>> %s\n" % description)
        
    def mark_local_complete(self):
        print "Local operations successfully completed. Initiating remote procedures."        
        self.file_obj.write("[LOCAL PROCEDURES COMPLETE]\n")
        self.reset_cp()

    def mark_local_checkpoint(self, desc):
        '''
        Marks a local checkpoint in the log.
        '''
        self.checkpoint_id += 1
        print "\nMarking local checkpoint %d ...\n" % self.checkpoint_id
        self.file_obj.write("[LOCAL CHECKPOINT::%d]>> %s\n" % (self.checkpoint_id, desc))

    def mark_server_checkpoint(self, ip):
        '''
        Marks the completion of operations of a specific server.
        '''
        print "Marking operations on server %s as successful." % ip
        self.file_obj.write("[SERVER CHECKPOINT::%s]\n" % ip)
        self.reset_cp()
        
    def mark_remote_checkpoint(self, desc, ip):
        '''
        Marks a remote checkpoint in the log.
        '''
        self.checkpoint_id += 1
        print "\nMarking remote checkpoint %s for server %s ...\n" % (self.checkpoint_id, ip)
        self.file_obj.write("[REMOTE CHECKPOINT::%s::%d]>> %s\n" % (ip, self.checkpoint_id, desc))
        
        
    def skip_checkpoint(self):
        '''
        Skips a checkpoint, usually because it was successfuly reached in last action which is being resumed,
         probably due to abrupt termination of the action.
        '''
        self.checkpoint_id += 1
        print "\nSkipping checkpoint %d...\n" % self.checkpoint_id
        self.file_obj.write("[SKIP CHECKPOINT::%d]\n" % self.checkpoint_id)
        

    def action_complete(self):
        '''
        Marks the completion of the action in the log file.
        '''
        print "Action completed successfully."
        self.file_obj.write("[ACTION_COMPLETE]>> %s\n" % datetime.now().isoformat())
        self.file_obj.close()
        
        
class LogChecker():
    '''
    Log file checker module that detects abrupt termination of program and extracts last successful checkpoint.
    '''
    def __init__(self, session):
        location = os.path.join("Logs", os.path.join(os.path.join(session["app_name"], "v%s" % session["version"]), "log"))
        self.log_f = open(location, "r").readlines()
        
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
        completed_servers = []
        partially_completed_servers = []
        servers_already_noted = set()
        lcomp_re = re.compile('^\[LOCAL PROCEDURES COMPLETE\]')
        scomp_re = re.compile('^\[SERVER CHECKPOINT::([\d\.]+)\]')
        sincomp_re = re.compile('^\[REMOTE CHECKPOINT::([\d\.]+)::(\d+)\]')
        while True:
            line = self.log_f[-i]
            completed_server = scomp_re.findall(line)
            incomplete_server = sincomp_re.findall(line)
            if completed_server:
                completed_servers.append((completed_server, 0))
            elif incomplete_server and (incomplete_server[0][0] not in completed_servers) and (incomplete_server[0][0] not in servers_already_noted):
                partially_completed_servers.append((incomplete_server[0][0], int(incomplete_server[0][1]))) 
                '''
                Above, the checkpoint is converted to int type before being appended.
                '''
                servers_already_noted.add(incomplete_server[0][0])
            elif lcomp_re.search(self.log_f[-i]):
                break
            i += 1
                
        return completed_servers, partially_completed_servers
            
            

    