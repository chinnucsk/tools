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
env.dchk = 'dc.hk.247realmedia.com'
amhome = '/var/home/appmgr'

sys.path.append(os.path.abspath('..'))
from common import *

def setpkg(ver, build):
    env.rpmlist = { 
        'lp'  :   (
            "tfsm-zama-lp-rt-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
        ),
    }



def stg():

    env.roledefs = {
                'lpmemc' :    ['rtblpmemc1us2-stg1.%s' % env.dcash],
                'lp' : [  'rtblp1us2-stg1.%s' % env.dcash,
                          'rtblp2us2-stg1.%s' % env.dcash,
                          'rtblp3us2-stg1.%s' % env.dcash,
                          'rtblp4us2-stg1.%s' % env.dcash
                       ]
                }
    env.e = "stg"


def qa():
    env.roledefs = {
                'lpmemc' :    ['rtblpmemc1us1-qa1.%s' % env.dcash],
                'lp' : [  'rtblp1us1-qa1.%s' % env.dcash,
                          'rtblp2us1-qa1.%s' % env.dcash
                       ]
                }
    env.e = "qa"  


def qa2():
    env.roledefs = {
                'lpmemc' :    ['rtblpmemc1us2-qa2.%s' % env.dcash],
                'lp' : [  'rtblp1us2-qa2.%s' % env.dcash,
                          'rtblp2us2-qa2.%s' % env.dcash
                       ]
                }
    env.e = "qa2"  



def prodec():
    env.roledefs = {
                'lp'   : [
                          'rtblp1us2.%s' % env.dcash,
                          'rtblp2us2.%s' % env.dcash,
                          'rtblp3us2.%s' % env.dcash,
                          'rtblp4us2.%s' % env.dcash,
                          'rtblp5us2.%s' % env.dcash,
                          'rtblp6us2.%s' % env.dcash
                         ]
                }

def prodams():
    env.roledefs = {
                'lp'   : [
                          'rtblp1eu1.%s' % env.dcams,
                          'rtblp2eu1.%s' % env.dcams
                         ]
                }


def prodhk():
    env.roledefs = {
                'lp'   : [
                         'rtblp1ap1.%s' % env.dchk
    #                      'rtblp2ap1.%s' % env.dchk
                         ]
                }

