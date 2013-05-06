import sys
import os
#import tarfile
from time import sleep
from fabric import decorators
from fabric.api import *
from fabric.contrib.files import exists, sed, append
from fabric.decorators import hosts

import shell
#env.user='root'
env.dcash = 'dc.ash.247realmedia.com'
env.dcams = 'dc.ams.247realmedia.com'
env.dclv = 'dc.lv.247realmedia.com'
amhome = '/var/home/appmgr'

sys.path.append(os.path.abspath('..'))
from common import *

def setpkg(ver, build):
    env.rpmlist = { 
        'rtbbid' : ( 
            "zama_mod_config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_vdb_config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_vdb_client-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
#            "zama_rtb_proxy_admeld-%s-bld%s.rh5.x86_64.rpm"  %(ver, build),
#            "zama_rtb_proxy_bidder_api-%s-bld%s.rh5.x86_64.rpm"  %(ver, build),
            "zama_rtb_proxy_appnexus-%s-bld%s.rh5.x86_64.rpm"  %(ver, build),
#            "zama_rtb_proxy_esm-%s-bld%s.rh5.x86_64.rpm"  %(ver, build),
#            "zama_rtb_proxy_ctxweb-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_rtb_proxy_google-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_rtb_proxy_rbc-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_rtb_proxy_pubmatic-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_rtb_proxy_openx-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
#            "zama_rtb_proxy_fb-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_tracker-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_click_tracker-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_conv_tracker-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_matcher-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_services-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_request_logger-%s-bld%s.rh5.x86_64.rpm" %(ver, build)
        ),
        'rtbmatch'  :  (
            "zama_click_tracker-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_conv_tracker-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_matcher-%s-bld%s.rh5.x86_64.rpm" %(ver, build)
        ),
        'rtbsloop'  :  (
#            "zama_vdb_config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
#            "zama_vdb_client-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
#            "zama_workflow-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_campaigns_publisher-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
#            "zama_bllistsync_publisher-%s-bld%s.rh5.x86_64.rpm" %(ver, build)
            ),
        'rtbmem' : (
            "zama_vdb_config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_services-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_workflow-%s-bld%s.rh5.x86_64.rpm" %(ver,build)
        ),
        'rtbscd' : (
            "tfsm-mr-schd-common-%s-bld%s.rh4.x86_64.rpm" %(ver,build),
            "tfsm-mr-config-%s-bld%s.rh4.x86_64.rpm" %(ver,build),
            "tfsm-mr-schd-ctrl-%s-bld%s.rh4.x86_64.rpm" %(ver,build),
            "tfsm-mr-schd-agent-%s-bld%s.rh4.x86_64.rpm" %(ver,build),
            "tfsm-mr-schd-api-%s-bld%s.rh4.x86_64.rpm" %(ver,build)
        ),
        'rtbvdb'  : (
            "zama_vdb_config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_vdb_service-%s-bld%s.rh5.x86_64.rpm" %(ver, build)
        ),
        'rtbvld'  : (
            "zama_vdb_config-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
            "zama_vdb_loader-%s-bld%s.rh5.x86_64.rpm" %(ver, build)
        ),

        
    }



def qa2():
  env.e = "qa2"
  env.roledefs = {
                 'rtbbid' :    [
                                'rtbbid1us2-qa2.%s' % env.dcash,
                                'rtbbid2us2-qa2.%s' % env.dcash
                               ],
                 'rtbsloop' : ['rtbsloop1us2-qa2.%s' %env.dcash
                              ],
                 'rtbmem' : ['rtbmem1us2-qa2.%s' %env.dcash,
                              'rtbmem2us2-qa2.%s' %env.dcash
                            ],
                 'rtbvdb' : ['rtbvln1us2-qa2.%s' %env.dcash
                            ],
                 'rtbvld' :    [
                                'rtbsloop1us2-qa2.%s' % env.dcash
                               ],
                 }



def qa():
  env.e = "qa"
  env.roledefs = {
                 'rtbbid' :    [
                                'rtbbid1us1-qa1.%s' % env.dcash,
                                'rtbbid2us1-qa1.%s' % env.dcash
#                                'rtbbid3us1-qa1.%s' % env.dcash
                               ],
                 'rtbvld' :    [
                                'rtbbid3us1-qa1.%s' % env.dcash
                               ],
                 'rtbsloop' : ['rtbsloop1us1-qa1.%s' %env.dcash
                              ],
                  'rtbmem' : ['rtbmem1us1-qa1.%s' %env.dcash,
                              'rtbmem2us1-qa1.%s' %env.dcash
                             ],
                  'rtbvdb' : ['rtbmdb1us1-qa1.%s' %env.dcash
                             ]

                 }


def stg():
  env.e = "stg"
  env.roledefs = {
                'rtbbid' :    [
                                'rtbbid1us2-stg1.%s' % env.dcash,
                                'rtbbid2us2-stg1.%s' % env.dcash,
                                'rtbbid3us2-stg1.%s' % env.dcash,
                                'rtbbid4us2-stg1.%s' % env.dcash
                              ],
                 'rtblp' :    [
                                'rtblp1us2-stg1.%s' % env.dcash,
                                'rtblp2us2-stg1.%s' % env.dcash,
                                'rtblp3us2-stg1.%s' % env.dcash,
                                'rtblp4us2-stg1.%s' % env.dcash
                           ],
                 'rtbvld' :    [
                                'rtbsloop1us2-stg1.%s' % env.dcash
                               ],
                 'rtbsloop' : [
                               'rtbsloop1us2-stg1.%s' %env.dcash
                              ],
                  'rtbmem' : [
                              'rtbmem1us2-stg1.%s' %env.dcash,
                              'rtbmem2us2-stg1.%s' %env.dcash
                             ],
                  'rtbvdb' : [
                              'rtbvln1us2-stg1.%s' %env.dcash
                             ]

                }


def esmdev():
  env.e = "esmdev"
  env.roledefs = {
                'rtbbid' :    [
                               'esmbid1us2-dev1.%s' % env.dcash,
                               'esmbid2us2-dev1.%s' % env.dcash,
                              ],
                 'rtblp' :    [
                                'esmlp1us2-dev1.%s' % env.dcash,
                                'esmlp2us2-dev1.%s' % env.dcash,
                                'esmlp3us2-dev1.%s' % env.dcash,
                                'esmlp4us2-dev1.%s' % env.dcash
                              ],
                 'rtbsloop' : [
                               'esmsloop1us2-dev1.%s' %env.dcash
                              ],
                  'rtbmem' : [
                               'esmmem1us2-dev1.%s' %env.dcash,
                               'esmmem1us2-dev1.%s' %env.dcash
                             ]

               }




def prodec():
  env.e = "prod_ec"
  env.roledefs = {
                'rtbbid' :    [
                              'rtbbid1us2.%s' % env.dcash
#                              'rtbbid2us2.%s' % env.dcash,
#                              'rtbbid3us2.%s' % env.dcash,
#                              'rtbbid4us2.%s' % env.dcash,
#                              'rtbbid5us2.%s' % env.dcash,
#                              'rtbbid6us2.%s' % env.dcash,
#                              'rtbbid7us2.%s' % env.dcash,
#                              'rtbbid8us2.%s' % env.dcash,
#                              'rtbbid9us2.%s' % env.dcash,
#                              'rtbbid10us2.%s' % env.dcash,
#                              'rtbbid13us2.%s' % env.dcash,
#                              'rtbbid14us2.%s' % env.dcash,
#                              'rtbbid15us2.%s' % env.dcash,
#                              'rtbbid16us2.%s' % env.dcash,
#                              'rtbbid17us2.%s' % env.dcash,
#                              'rtbbid18us2.%s' % env.dcash,
#                              'rtbbid19us2.%s' % env.dcash,
#                              'rtbbid20us2.%s' % env.dcash
                              ] ,
                 'rtbsloop' : ['rtbsloop2us2.%s' %env.dcash
                              ],
                 'rtbmem' :  ['rtbmem1us2.%s' %env.dcash,
                              'rtbmem2us2.%s' %env.dcash
                             ]

                }
  print(red("!WARNING! Working on East Coast ZT production !WARNING!"))
  ans=prompt("Are you sure you want to continue", default="N")

def prodwc():
  env.e = "prod_wc"
  env.roledefs = {
                'rtbbid' :    [
#                              'rtbbid1us3.%s' % env.dclv,
                              'rtbbid2us3.%s' % env.dclv,
                              'rtbbid3us3.%s' % env.dclv,
                              'rtbbid4us3.%s' % env.dclv,
                              'rtbbid5us3.%s' % env.dclv,
                              'rtbbid6us3.%s' % env.dclv,
#                              'rtbbid7us3.%s' % env.dclv,
#                              'rtbbid8us3.%s' % env.dclv
                              ] , 
                 'rtbsloop' : ['rtbsloop1us3.%s' %env.dclv
                              ],
                 'rtbmem' :  ['rtbmem1us3.%s' %env.dclv,
                              'rtbmem2us3.%s' %env.dclv
                             ]

                }
  print(red("!WARNING! Working on West Coast ZT production !WARNING!"))
  ans=prompt("Are you sure you want to continue", default="N")




def prodams():
  env.e = "prod_ams"
  env.roledefs = {
                'rtbbid' :    [
#				'rtbbid1eu1.%s' % env.dcams
                                'rtbbid2eu1.%s' % env.dcams,
                                'rtbbid3eu1.%s' % env.dcams,
                                'rtbbid4eu1.%s' % env.dcams
                              ],
                'rtblp' :     ['rtblp1eu1.%s' % env.dcams,
                               'rtblp2eu1.%s' % env.dcams
                              ],
                'rtbsloop' : ['rtbsloop1eu1.%s' %env.dcams
                              ],

                }
  print(red("!WARNING! Working on EU ZT production !WARNING!"))
  ans=prompt("Are you sure you want to continue", default="N")





