'''
Created on 18-Feb-2014

@author: Abhimanyu
'''

import re

sincomp_re = re.compile('^\[REMOTE CHECKPOINT::([\d\.]+)::(\d+)\]')

s = '''
[ACTION_BEGIN]>> deploy : Abhimanyu : 2014-04-22T13:36:14.311722
    SUBPROCESS>> Gathering alphainstaller settings.
    SUBPROCESS>> Gathering information about app2 version 4.7.
    SUBPROCESS>> Checking out data from repository.
[LOCAL CHECKPOINT::1]>> Checked out repository
    SUBPROCESS>> Building code base.
[LOCAL CHECKPOINT::2]>> Codebase built
    SUBPROCESS>> Compressing files for deployment.
[LOCAL CHECKPOINT::3]>> Files compressed
[LOCAL PROCEDURES COMPLETE]
    SUBPROCESS>> Deploying app on server : 10.164.253.216
    SUBPROCESS>> Setting up SSH connection with 10.164.253.216
    SUBPROCESS>> Setting up SCP client.
    SUBPROCESS>> Sending files.
[REMOTE CHECKPOINT::10.164.253.216::1]>> Package successfully uploaded.
    SUBPROCESS>> Extracting 'alphainstaller.tar.gz'
'''

i = 1

log_f = open("Logs/app2/v4.7/log", "r").readlines()
completed_servers = []
partially_completed_servers = []
servers_already_noted = set()
lcomp_re = re.compile('^\[LOCAL PROCEDURES COMPLETE\]')
scomp_re = re.compile('^\[SERVER CHECKPOINT::([\d\.]+)\]')
sincomp_re = re.compile('^\[REMOTE CHECKPOINT::([\d\.]+)::(\d+)\]')
while True:
    line = log_f[-i]
    completed_server = scomp_re.findall(line)
    incomplete_server = sincomp_re.findall(line)
    if completed_server:
        completed_servers.append((completed_server, 0))
    elif incomplete_server and (incomplete_server[0][0] not in completed_servers) and (incomplete_server[0][0] not in servers_already_noted):
        partially_completed_servers.append(incomplete_server[0])
        servers_already_noted.add(incomplete_server[0][0])
    elif lcomp_re.search(log_f[-i]):
        break
    i += 1
        
print completed_servers
print partially_completed_servers




