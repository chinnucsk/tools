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
        'rtx'  :   (
            "tfsm-esmeralda-be-engine-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-esmeralda-config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-esmeralda-oraclient-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "tfsm-esmeralda-stat_collector-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
        ),
        'esmlp'  :   (
            "tfsm-esmeralda-lp-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
        ),
        'esmtools'  :   (
            "tfsm-esmeralda-tools-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
        ),
        'esmlpmemc'  :   (
            "tfsm-esmeralda-lp-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
        ),

    }


def qa():
 env.e = "qa"
 amhome = '/var/home/appmgr/tfsm/'
 env.roledefs = {
                'rtx' : ['esmrtx1us2-sb1',
                         'esmrtx2us2-sb1.%s' % env.dcash,
                        ],
               'esmlp' :    ['esmlp1us2-qa1.%s' % env.dcash,
                         ],
               'esmlpmemc' :    ['esmlpmemc1us2-qa1.%s' % env.dcash,
                         ],
               'esmlgc' :    ['esmlgc1us2-qa1.%s' % env.dcash,
                         ]
                }
def qa2():
 env.e = "qa2"
 amhome = '/var/home/appmgr/tfsm/'
 env.roledefs = {
               'rtx' :  ['esmrtx1us2-qa2.%s' % env.dcash,
                         'esmrtx2us2-qa2.%s' % env.dcash,
                        ],
               'esmlp' :    ['esmlp1us2-qa2.%s' % env.dcash,
                         ],
               'esmlpmemc' :    ['esmlpmemc1us2-qa2.%s' % env.dcash,
                         ],
               'esmlgc' :    ['esmlgc1us2-qa2.%s' % env.dcash,
                         ]
                }



def prod():
 env.e = "prod"
 amhome = '/var/home/appmgr/'
 env.roledefs = {
                'rtx' : [
                         'esmrtx1us2',
                         'esmrtx2us2',
                         'esmrtx3us2',
                         'esmrtx1us1',
                         'esmrtx2us1',
                         'esmrtx3us1'
                        ],
               'esmlp' :     [
                               'esmlp2us2',
                             ],
               'esmlpmemc' : [
                              'esmlpmemc1us2',
                             ],
               'esmlgc' :    [
                              'esmlgc1us2',
			      'esmlgc1us1'
                             ]
                }


def prod_eu():
 env.e = "prod_eu"
 amhome = '/var/home/appmgr/'
 env.roledefs = {
                'rtx' : [
                         'esmrtx1eu2',
                         'esmrtx2eu2'
                        ],
               'esmlp' :     [
                               'esmlp1eu2'
                             ],
               'esmlpmemc' : [
                              'esmlpmemc1eu2'
                             ],
               'esmlgc' :    [
                              'esmlgc1eu2'
                             ]
                }

