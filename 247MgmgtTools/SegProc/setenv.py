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
                       'gps'  :  ( 
                                   "gps-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
                                 ),
                       'segPApi' : (
                                   "zama_gp__lookalike_webservice-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
                                   ),
                       'segProc' : (
                                   "zama_gp__segment_processing-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
	                           ),
                       'TargAd' : (
                                   "zama_targad__segment_integration-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
	                           )
                  }


def qa():
    env.e = "qa"  
    env.roledefs = {
                'segProc' : [  
                          'seggen1us2-qa1.%s' % env.dcash,
                          'seggen2us2-qa1.%s' % env.dcash,
                          ],
                'segPApi' : [  
                          'rtbll1us1-qa1.%s' % env.dcash
                          ],
#                'TargAd' : [  
#                          'seggen1us2-qa1.%s' % env.dcash
#                          ],

               }
def qa2():
    env.e = "qa"  
    env.roledefs = {
                'segPApi' : [  
                          'rtbll1us2-qa2.%s' % env.dcash
                       ]
               }


def prod():
    env.e = "prod"  
    env.roledefs = {
               'segProc' : [  
                          'seggen1us2.%s' % env.dcash,
                          'seggen2us2.%s' % env.dcash
                       ],
               'segPApi' : [  
                          'rtbll1us2.%s' % env.dcash
                       ]
               }

def stg():
    env.e = "stg"  
    env.roledefs = {
               'segProc' : [  
                          'seggen1us2-stg1.%s' % env.dcash,
                          'seggen2us2-stg1.%s' % env.dcash
                       ],
               'segPApi' : [  
                          'rtbll1us2-stg1.%s' % env.dcash
                       ]
               }


def prod_ams():
    env.e = "prod_eu"  
    env.roledefs = {
               'segPApi' : [  
                           'rtbll1eu1.%s' % env.dcams
                           ]
               }
