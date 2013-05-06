import os
import datetime
import sys
import tarfile
from time import sleep
from fabric.api import *
from fabric.colors import *
from fabric import decorators
from fabric.decorators import hosts
from setenv import *


apidbconfs = [
            '/var/home/appmgr/java/cfg/RTB/db.properties',
            '/usr/local/tomcat/conf/context.xml'
           ]


env.config_file = 'config.yaml'
env.user = 'pkatsovich'
env.dcash = 'dc.ash.247realmedia.com'
amhome = '/var/home/appmgr'

    
sys.path.append(os.path.abspath('..'))
from common import *


@roles('rtbscd')
def upScd(ver='None', bld='None'):
    if ver is not 'None':
     with settings(warng_only=True):
       tmppath=sendrpms("mig_reporting", 'rtbscd', ver, bld)
       sudo("rpm -Uvh %s/*.rpm" %(tmppath))
       sudo("/etc/init.d/httpd restart")
    else:
       print "You forgot to specify version i.e 002"


@roles('dashMap')
def upDashMap(ver='None', bld='None'):
    if ver is not 'None':
     with settings(warng_only=True):
       tmppath=sendrpms("zama_dashboard", "dashMap", ver, bld)
       sudo("rpm -Uvh %s/*.rpm" %(tmppath))
       sudo("/etc/init.d/httpd restart")
    else:
       print "You forgot to specify version i.e 002"
   




@roles('ztDash')
def upDash(ver='None', bld='None'):
    if ver is not 'None':
       setpkg(ver, bld)
       tmppath=sendrpms("zama_dashboard", "ztDash", ver, bld, "5")
       sudo("/etc/init.d/tomcat stop")
       time.sleep(5)
       sudo("ps aux | grep java")
       stopTomcat()
       with cd("%s" %env.tomcat):
           sudo("rm -rf webapps/dashboard/")
           sudo("rm -rf Work/Catalina")
    #   startTomcat()
       #sudo("rpm -qa | grep tfsm-zama-dashboard | xargs rpm -e")
       sudo("ln -sf /var/home/appmgr/tfsm/zama/dashboard/api/trader/wars/dashboard.war /opt/tomcat/webapps/", user="appmgr")
       sudo("rpm -Uvh --force --replacepkgs %s/*.rpm" %(tmppath))
    #   startTomcat()
    else:
       print "Did you forgot to specify version i.e 002"
    

def confExists(role='None'):
 if role is not 'None':     
    for  config in env.confs[role]:
         if exists(config):
                print(blue("%s " %config)) 
         else:
                print(red("%s " %config)) 
                print(red("CONFIG FILE MISING")) 


def installCommonUI(ver='None', bld='None'):
   setpkg(ver, bld)
   print ver
   tmppath = sendrpms("Common_UI", "common_ui", ver, bld, "4")
   sudo("rpm -Uvh --prefix=/var/home/appmgr/tfsm/ %s/*.rpm" %(tmppath))

