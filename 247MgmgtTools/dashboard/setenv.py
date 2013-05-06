import sys
import os
#import tarfile
from time import sleep
from fabric import decorators
from fabric.api import *
from fabric.contrib.files import exists, sed, append
from fabric.decorators import hosts

#env.user='root'
env.dcash = 'dc.ash.247realmedia.com'
env.dcams = 'dc.ams.247realmedia.com'
env.dclv = 'dc.lv.247realmedia.com'
amhome = '/var/home/appmgr'

sys.path.append(os.path.abspath('..'))
from common import *

def setpkg(ver, build):
    env.rpmlist = { 
       'common_ui' : (
	    "tfsm-common-ui-js-yui3-%s-bld%s.rh4.x86_64.rpm" %(ver, build),
            "tfsm-common-ui-js-util-%s-bld%s.rh4.x86_64.rpm" %(ver, build),
	    "tfsm-common-ui-js-yui2in3-%s-bld%s.rh4.x86_64.rpm" %(ver, build),
       ),
       'ztDash'  :   (
            "tfsm-zama-dashboard-config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-api-trader-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-notification_manager-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-ui-common-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-ui-trader-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-ui-comboloader-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
       ),
        'dashMap'  :   (
            "tfsm-zama-dashboard-config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-mapping-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-mapping-world-layer-%s-bld%s.rh5.x86_64.rpm" %(ver, build)
        ),
    }

def prod():
    env.tomcat = "/opt/tomcat"
    env.roledefs = {
                    'dashMap' :    [ 'rtbdash1us1'
                                   ],
                    'ztDash' :      [
                                      'rtbui3us1',
                                      'rtbui4us2'
                                   ]
                   }

    env.confs = {
                    'dashApi'  :   [ '/var/home/appmgr/tfsm/zama/conf/dashboard-api/dashboard-api.properties',
                                     '/usr/local/tomcat/lib/dashboard-api.properties',
				     '/var/home/appmgr/tfsm/zama/notifications_manager/conf/databaseconf.properties',
                                     '/var/home/appmgr/tfsm/zama/conf/dashboard-ui/zama-dashboard.include'
                                   ],

                    'dashMap' :    [ '/var/home/appmgr/tfsm/zama/conf/dashboard-mapping/tilestache.cfg'
                                   ]
		   }


def prod_hk():
    env.tomcat = "/opt/tomcat"
    env.roledefs = {
                    'dashMap'  : ['rtbdash1eu1',
				 ],
	            'rtbscd' :     [ 'rtbscd1eu1'
                                   ],
                    'ztDash' :      [
                                      'rtbui3ap1',
                                      'rtbui4ap1'
                                   ]
                   }
    env.confs = {
                    'dashApi'  :   [ '/var/home/appmgr/tfsm/zama/conf/dashboard-api/dashboard-api.properties',
                                     '/usr/local/tomcat/lib/dashboard-api.properties',
				     '/var/home/appmgr/tfsm/zama/notifications_manager/conf/databaseconf.properties',
                                     '/var/home/appmgr/tfsm/zama/conf/dashboard-ui/zama-dashboard.include'
                                   ],

                    'dashMap' :    [ '/var/home/appmgr/tfsm/zama/conf/dashboard-mapping/tilestache.cfg'
                                   ]
		   }




def prod_ams():
    env.tomcat = "/opt/tomcat"
    env.roledefs = {
                    'dashMap'  : ['rtbdash1eu1',
				 ],
	            'rtbscd' :     [ 'rtbscd1eu1'
                                   ],
                    'ztDash' :      [
                                      'rtbui3eu1',
                                      'rtbui4eu1'
                                   ]
                   }
    env.confs = {
                    'dashApi'  :   [ '/var/home/appmgr/tfsm/zama/conf/dashboard-api/dashboard-api.properties',
                                     '/usr/local/tomcat/lib/dashboard-api.properties',
				     '/var/home/appmgr/tfsm/zama/notifications_manager/conf/databaseconf.properties',
                                     '/var/home/appmgr/tfsm/zama/conf/dashboard-ui/zama-dashboard.include'
                                   ],

                    'dashMap' :    [ '/var/home/appmgr/tfsm/zama/conf/dashboard-mapping/tilestache.cfg'
                                   ]
		   }


def qa():
    env.tomcat = "/opt/tomcat"
    env.roledefs = {
                    'dashMap' :    [ 'rtbdash1us2-qa1'
                                   ],
                    'rtbscd' :     [ 'rtbscd1us1-qa1'
                                   ],
                    'ztDash' :      [
                                      'rtbui2us1-qa1',
                                      'rtbui3us1-qa1'
                                   ]
		   }

    env.confs = {
                    'dashApi'  :   [ '/var/home/appmgr/tfsm/zama/conf/dashboard-api/dashboard-api.properties',
                                     '/usr/local/tomcat/lib/dashboard-api.properties',
				     '/var/home/appmgr/tfsm/zama/notifications_manager/conf/databaseconf.properties',
                                     '/var/home/appmgr/tfsm/zama/conf/dashboard-ui/zama-dashboard.include'
                                   ],

                    'dashMap' :    [ '/var/home/appmgr/tfsm/zama/conf/dashboard-mapping/tilestache.cfg'
                                   ]
		   }




def qa2():
    env.tomcat = "/opt/tomcat"
    env.roledefs = {
                    'ztDash'  :   [ 'rtbui1us2-qa2',
                                     'rtbui2us2-qa2'
                                   ],
                    'dashMap' :    [ 'rtbdash1us2-qa2'
                                   ],
		   }

    env.confs = {
                    'dashApi'  :   [ '/var/home/appmgr/tfsm/zama/conf/dashboard-api/dashboard-api.properties',
                                     '/usr/local/tomcat/lib/dashboard-api.properties',
				     '/var/home/appmgr/tfsm/zama/notifications_manager/conf/databaseconf.properties',
                                     '/var/home/appmgr/tfsm/zama/conf/dashboard-ui/zama-dashboard.include'
                                   ],

                    'dashMap' :    [ '/var/home/appmgr/tfsm/zama/conf/dashboard-mapping/tilestache.cfg'
                                   ]
		   }




def stg():
    env.tomcat = "/opt/tomcat"
    env.roledefs = {
                    'dashMap' :    [ 'rtbdash1us2-qa1'
                                   ],

                    'ztDash'  :   [ 'rtbui3us2-stg1',
                                  ]
		   }


    env.confs = {
                    'dashApi'  :   [ '/var/home/appmgr/tfsm/zama/conf/dashboard-api/dashboard-api.properties',
                                     '/usr/local/tomcat/lib/dashboard-api.properties',
				     '/var/home/appmgr/tfsm/zama/notifications_manager/conf/databaseconf.properties',
                                     '/var/home/appmgr/tfsm/zama/conf/dashboard-ui/zama-dashboard.include'
                                   ],

                    'dashMap' :    [ '/var/home/appmgr/tfsm/zama/conf/dashboard-mapping/tilestache.cfg'
                                   ]
		   }



