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
        'dashApi'  :   (
            "tfsm-zama-dashboard-config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-api-trader-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-notification_manager-%s-bld%s.rh5.x86_64.rpm" %(ver, build)
        ),
        'dashClient'  :   (
            "tfsm-zama-dashboard-config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-ui-common-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-ui-trader-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
        ),
        'dashMap'  :   (
            "tfsm-zama-dashboard-config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-mapping-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-zama-dashboard-mapping-world-layer-%s-bld%s.rh5.x86_64.rpm" %(ver, build)
        ),
        'Common_UI' : (
            "tfsm-common-ui-js-yui3-%s-bld%s.rh4.x86_64.rpm" %(ver, build),
            "tfsm-common-ui-js-util-%s-bld%s.rh4.x86_64.rpm" %(ver, build),
            "tfsm-common-ui-js-yui2in3-%s-bld%s.rh4.x86_64.rpm" %(ver, build),
        ),

    }



def prod():
    env.dc = ".dc.ash.247realmedia.com"
    env.tomcat = "/usr/local/tomcat"
    env.e = "prod_ec"
    env.roledefs = {
        'flex'  : [
            'rtbflex1us2',
            'rtbflex2us2'
        ],
        'api'   : [
            'rtbapi1us2',
            'rtbapi2us2'
        ],
        'ztui' : [
            'rtbui3us1%s' %env.dc
#            'rtbui4us2%s' %env.dc
        ],

    }



def prod_ams():
    env.e = "prod_eu"
    env.dc = ".dc.ams.247realmedia.com"
    env.tomcat = "/opt/tomcat"
    env.roledefs = {
        'flex'  : [
            'rtbflex1eu1',
            'rtbflex2eu1'
        ],
        'api'   : [
            'rtbapi1eu1',
            'rtbapi2eu1'
        ],
        'ztui' : [
            'rtbui3eu1%s' %env.dc
#            'rtbui4eu1%s' %env.dc
        ],

    }

def prod_hk():
    env.e = "prod_hk"
    env.dc = ".dc.hk.247realmedia.com"
    env.tomcat = "/opt/tomcat"
    env.roledefs = {
        'flex'  : [
            'rtbflex1ap1',
            'rtbflex2ap1'
        ],
        'api'   : [
            'rtbapi1ap1',
            'rtbapi2ap1'
        ],
        'ztui' : [
            'rtbui3ap1%s' %env.dc,
            'rtbui4ap1%s' %env.dc
        ],

    }



def qa():
    env.tomcat = "/usr/local/tomcat"
    env.roledefs = {
        'api'   : [
            'rtbapi1us1-qa1',
            'rtbapi2us1-qa1'
        ],
        'flex'  : [ 
            'rtbflex1us1-qa1'
        ],
        'ztui' : [
            'rtbui2us1-qa1',
            'rtbui3us1-qa1'
        ],
    }

def qa2():
    env.tomcat = "/usr/local/tomcat"
    env.e = "qa2"
    env.roledefs = {
        'api'    : [
            'rtbapi1us2-qa2',
            'rtbapi2us2-qa2'
        ],
        'flex'   : [
            'rtbflex1us2-qa2'
        ],
        'ztui' : [
            'rtbui1us2-qa2',
            'rtbui2us2-qa2'
        ],
   }



def stg():
    env.tomcat = "/opt/tomcat"
    env.roledefs = {
        'api'   : [
            'rtbapi1us2-stg1'
        ],
        'flex'   : [
            'rtbflex1us2-stg1'
        ],
        'ztui' : [
            'rtbui3us2-stg1',
        ],

      }

