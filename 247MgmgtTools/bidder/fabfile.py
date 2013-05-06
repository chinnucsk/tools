import sys
import os
#import tarfile
from time import sleep
from fabric import decorators
from fabric.api import *
from fabric.contrib.files import exists, sed, append
from fabric.decorators import hosts
from setenv import *

import shell
#env.user='root'
env.dcash = 'dc.ash.247realmedia.com'
env.dcams = 'dc.ams.247realmedia.com'
env.dclv = 'dc.lv.247realmedia.com'
amhome = '/var/home/appmgr'

sys.path.append(os.path.abspath('..'))
from common import *




@roles('rtbbid')
def installBID(ver="None", bld="None"):
  '''Install Bidder from scratch, includes apache, create appmgr user, install all bidder packages
  '''
  if ver is 'None':
    print "You forgot version or Build #"
  else:
    setpkg(ver, bld)
    installhttpd()
    addUser("appmgr")
    if not exists('/etc/httpd/conf.d'):
       sudo('mkdir -p /etc/httpd/conf.d')     
    upgradeBid(ver, bld)


@roles('rtbbid')
def upgradeBid(ver="None", bld="None"):
  '''Upgrade ZTBidder, requires Version and Build to be passed.
  '''
  apps=["rtbbid"]
  if ver is 'None':
    print "You forgot version or Build #"
  else:
    setpkg(ver, bld)
    svn_co()
    for app in apps:
      tmppath=sendrpms("zama_bid", app , ver, bld, rh="5")
      put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath)
      with settings(warn_only = True):
          with cd("%s" %tmppath):
            stopBID()
            sudo("rpm -e zama_conv_tracker-12.0-bld007.rh5")
            sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh ZAMA_APACHE_CONF=/etc/httpd/conf ZAMA_APACHE_MODULES=/usr/lib64/httpd/modules rpm -Uvh --replacepkgs --replacefiles --prefix=%s  %s/*.rpm" %(tmppath, env.e, amhome, tmppath))
  sudo("/root/zama_start.sh")


@roles('rtbsloop')
def upgradeSloop(ver="None", bld="None"):
  if ver is 'None':
    print "You forgot version or Build #"
  else:
   setpkg(ver, bld)
   installtbb()
   tmppath=sendrpms("zama_bid", "rtbsloop", ver, bld, rh="5")
   put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath) 
   sudo("/root/zama_stop.sh")
   sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh rpm -Uvh --replacepkgs --prefix=%s %s/*.rpm" %(tmppath, env.e, amhome, tmppath))
   sudo("/root/zama_start.sh")


@roles('rtbmem')
def upgradeStcol(ver="None", bld="None"):
  if ver is 'None':
    print "You forgot version or Build #"
  else:
   setpkg(ver, bld)
   installtbb()
   tmppath=sendrpms("zama_bid","rtbmem", ver, bld, rh="5")
#   svn_co()
   sudo("/root/zama_stop.sh")
   put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath) 
#   sudo("rpm -qa | grep zama | xargs rpm -e")
   sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh rpm -Uvh --replacepkgs --prefix=%s %s/*.rpm" %(tmppath, env.e, amhome, tmppath))
   sudo("/root/zama_start.sh")


@roles('rtbvdb')
def upgradeVdb(ver="None", bld="None"):

    if ver is 'None':
        print "You forgot version or Build #"
    else:
        setpkg(ver, bld)
        tmppath=sendrpms("zama_bid", "rtbvdb", ver, bld, rh="5")
        svn_co()
        put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath) 
        put("dev/config/violin/qa/%s_vdb_layout-01.xml" %env.e, "%s" %tmppath)
        put("dev/config/violin/qa/%s_vdb_svc_config.xml" %env.e, "%s" %tmppath)
        sudo("cp %s/%s_vdb_layout-01.xml /var/home/appmgr/zama/conf/" %(tmppath, env.e))
        sudo("cp %s/%s_vdb_svc_config.xml /var/home/appmgr/zama/conf/" %(tmppath, env.e))
        with settings(warn_only="True"):
            sudo("/etc/init.d/vdbd stop")
            sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh rpm -Uvh --replacepkgs --prefix=%s %s/*.rpm" %(tmppath, env.e, amhome, tmppath))
            sudo("/etc/init.d/vdbd start")


@roles('rtbvdb')
def fixVDB():
   svn_co()
   tmppath="/tmp/"
   put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath) 
   put("dev/config/violin/qa/%s_vdb_layout-01.xml" %env.e, "%s" %tmppath)
   put("dev/config/violin/qa/%s_vdb_svc_config.xml" %env.e, "%s" %tmppath)
   sudo("cp %s/%s_vdb_layout-01.xml /var/home/appmgr/zama/conf/" %(tmppath, env.e), user="appmgr")
   sudo("cp %s/%s_vdb_svc_config.xml /var/home/appmgr/zama/conf/" %(tmppath, env.e), user="appmgr")
   with settings(warn_only="True"):
       sudo("/etc/init.d/vdbd stop")
#       sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh rpm -Uvh --replacepkgs --prefix=%s %s/*.rpm" %(tmppath, env.e, amhome, tmppath))
       sudo("/etc/init.d/vdbd start")


@roles('rtbvld')
def upgradeVLD(ver="None", bld="None"):

  if ver is 'None':
    print "You forgot version or Build #"
  else:
   setpkg(ver, bld)
   tmppath=sendrpms("zama_bid", "rtbvld", ver, bld, rh="5")
   svn_co()
   put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath) 
   with settings(warn_only="True"):
       sudo("/etc/init.d/vdbd stop")
       sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh rpm -Uvh --replacepkgs --prefix=%s %s/*.rpm" %(tmppath, env.e, amhome, tmppath))
       sudo("/etc/init.d/vdbd start")


#@roles('rtbbid')
def startBID():
        sudo("rm -rf /etc/httpd/conf.d/mod_rtb_yahoo.conf")
        checkUsrProc()
        rate = 0
#        rate = run("/usr/local/bin/bid_rate.sh")
        if rate == 0:
             print "Starting bidder, current bid rate is :%s" %rate
             sudo("echo OK > /var/www/html/status.txt")
             sudo("/etc/init.d/httpd start")
             sudo("%s/zama/bin/start.sh rtb_config.xml rtb" % amhome, user="appmgr")
             checkUsrProc()
#             time.sleep(5)
#             rate = run("/usr/local/bin/bid_rate.sh")
        
#        counter = 10
#        rate = 0
#        while (rate == 0) and (counter > 0):
#             print "bid rate is still 0"
#             rate = run("/usr/local/bin/bid_rate.sh")


#@roles('rtbbid')
def stopBID():
#        sudo("%s/zama/bin/stop.sh rtb" % amhome, user="appmgr")
       sudo("echo DOWN > /var/www/html/status.txt")
       rate = 2 
       while rate > 2:
             time.sleep(5)
             rate = run("/usr/local/bin/bid_rate.sh")
             print rate
             print "Sleeping 5 sec, Bid rate is still :%s" %rate
       
       if rate < 3:
             print "Stopping bidder, bid rate is :%s" %rate
             sudo("/etc/init.d/httpd stop")
             sudo("/var/home/appmgr/zama/bin/stop.sh rtb", user="appmgr")
             checkUsrProc()
          
@runs_once
def svn_co():
    local("rm -rf dev")
    local("svn co svn://172.16.16.21/TFSM/zama_ops/main/dev")


def cmd():
    shell.shell()


def checkUsrProc(user="appmgr"):
  '''check if LP is running'''
  with settings(warn_only = True):
   sudo("ps -ef | grep  %s " % user)




def startIDGEN():
    sudo("/etc/init.d/tfsm-id-gen-daemon restart")

def quick():
    sudo("rm -rf /var/home/appmgr/zeus" )
