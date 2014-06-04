'''
Created on 18-Feb-2014

@author: Abhimanyu
'''

from datetime import datetime
from apscheduler.scheduler import Scheduler

# Start the scheduler
sched = Scheduler(standalone=True)


# Define the function that is to be executed
def my_job(text):
    
    print text

# The job will be executed on November 6th, 2009
exec_date = datetime.strptime("2014-05-06 18:17:00", "%Y-%m-%d %H:%M:%S")

# Store the job in a variable in case we want to cancel it
job = sched.add_date_job(my_job, exec_date, ['sdasda'])
sched.start()