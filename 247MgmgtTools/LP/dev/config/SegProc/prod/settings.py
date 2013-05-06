############################
# Common Settings
# This part is used by both gpsd and bsd programs
############################

"""
 Log level, ["DEBUG", "INFO", "WARNING", "ERROR"]
 DEBUG shows everything while ERROR shows the minimum
 The recommended value is INFO
"""
LOG_LEVEL = 'INFO'

############################
# Batch Server Settings
# This part is only used by the slave (bsd)
############################

"""
The name of the server instances running in this host.
"""
BS_NAME = "seggen1us2"

"""
Default working directory (if not specified in the flow or the job)
"""
DEFAULT_WORKDIR = "/tmp"

"""
RESOURCES Conf overwrite from the agent
"""
RESOURCES = {'max_jobs': 1000,
             'local_resources': {'cpu': 900, 'mem': 58, 'io': 30},
             'shared_resources' : ['db_load', 'extraction_limit', 'bulk_extraction_limit']
             }

"""
How to handle the tasks standard and error output
Possible values:
PIPE: Buffurize the output and store it in the DB when the task is done
      /!\ Only if your output is short. If the size of the output fill the pipe buffer, the task will hang
FILE: Redirect both standard and error output to a file located in the TASK_OUTPUT_FILE directory provided bellow.
NONE: Do nothing with the outputs (i.e. redirecting to /dev/null)
"""
TASK_OUTPUT_HANDLER = 'FILE'

"""
The directory to store the tasks outputs if the FILE handler is selected
"""
FILE_TASK_OUTPUT_DIR = "/var/home/appmgr/gps/log/tasks"


############################
# Master Settings
# This part in only loaded by the scheduler (gpsd)
############################

"""
Shared vitrual resources list
Specify here all the global virtual resources.
A global resources share the count over all assigned servers.
"""
SHARED_RESOURCES = {'db_load': 6, 'extraction_limit': 1, 'bulk_extraction_limit': 1}
LOCAL_RESOURCES = ['io', 'cpu', 'root', 'master', 'proxy', 'mem']



"""
The batch server list.
Define all slaves whre you want to schedule jobs on here.
Assign local and shared resources to each servers.
A max value has to be associated to each local_resource.
"""

BATCH_SERVERS = {}

"""
The scheduling sleep interval in seconds
The scheduling process will wait this time until trying to pull finished jobs back.
"""
SCHEDULE_TIME = 2

"""
Setup the nofitications here
There is 2 types of builtin notifications: logfile and sendmail.
"""
NOTIFICATIONS= {'logfile': {'file': "/tmp/gps_notifications.log",
                            },
                'sendmail':{'smtp': "sysapp1.dc.ash.247realmedia.com",

                            'emails': ["sebastien.claeys@247realmedia.com",
                                       "jean-pierre.ocalan@247media.com",
                                       "Gisha.George@247realmedia.com",
                                       "nagesh.jatti@synechron.com",
                                      ],
                            'from': "seggenqa1@247realmedia.com",
                            },
                }

"""
In addition to the logfile and sendmail notification, GPS comes with a custom notiofication mechanism
User notifications allow you to call your own script/command as a notification.
The following environment variables will be available:
* GPS_EVENT_TYPE
* GPS_JOB_ID
* GPS_JOB_NAME
* GPS_FLOW_ID
* GPS_FLOW_NAME
* GPS_JOB_RETURNCODE
* GPS_JOB_STATUS
* GPS_JOB_STDOUT
* GPS_JOB_STDERR
* GPS_JOB_START
* GPS_JOB_END

As an example,
See the custom logfile and sendmail notification bellow
"""
USER_NOTIFICATIONS={'my_logfile': "echo \"The job <$GPS_JOB_ID> $GPS_EVENT_TYPE\" >> /tmp/my_logfile.out ",
                    'my_sendmail': "echo \"The job <$GPS_JOB_ID> $GPS_EVENT_TYPE\" | mail -s \"$GPS_JOB_ID $GPS_EVENT_TYPE\" sebastien.claeys@247realmedia.com",}
