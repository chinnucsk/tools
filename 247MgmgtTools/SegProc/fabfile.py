import os
import datetime
import sys
import tarfile
from time import sleep
from fabric.api import *
from fabric.contrib.files import exists, sed, append
from setenv import *
sys.path.append(os.path.abspath('..'))

from common import *


env.config_file = 'config.yaml'
#env.user = 'pkatsovich'
env.dcash = 'dc.ash.247realmedia.com'
env.dcams = 'dc.ams.247realmedia.com'
amhome = '/var/home/appmgr'



def holdFlows():
    with cd("/var/home/appmgr/gps"):
        sudo("./gps hold segment_processing", user="appmgr")
        sudo("./gps hold tp_seg_extraction", user="appmgr")
        sudo("./gps hold segmentation_ZT_US", user="appmgr")
        sudo("./gps hold segmentation_ZT_EU", user="appmgr")
        sudo("./gps hold segmentation_ZT_HK", user="appmgr")
        sudo("./gps hold dgen", user="appmgr")
        sudo("./gps hold daily_cleanup", user="appmgr")
        with settings(warn_only=True):
            while True:
                rsl=sudo("./gps flow | grep Running", user="appmgr").return_code
                print(blue(rsl))
                if rsl is 0:
                    print(red("Flow still running"))
                else:
                    print(green("flow is done"))
                    break


def submitFlows():
    with cd("/var/home/appmgr/zama_gp/segment_processing/"):
        sudo("./scripts/job_manager.py -j segment_processing -o ./jobs -t ./templates/segment_processing_daily.xml", user="appmgr")
        sudo("./scripts/job_manager.py -j dgen -o ./jobs -t ./templates/dgen.xml", user="appmgr")
        sudo("./scripts/job_manager.py -j tp_seg_extraction -o ./jobs -t ./templates/tp_segment_extraction_daily.xml", user="appmgr")



def releaseFlows():
    with cd("/var/home/appmgr/gps"):
        sudo("./gps release segment_processing", user="appmgr")
        sudo("./gps release tp_seg_extraction", user="appmgr")
        sudo("./gps release segmentation_ZT_US", user="appmgr")
        sudo("./gps release segmentation_ZT_EU", user="appmgr")
        sudo("./gps release segmentation_ZT_HK", user="appmgr")
        sudo("./gps release daily_cleanup", user="appmgr")
        sudo("./gps release dgen", user="appmgr")


@roles("segProc")
def installSegProc(ver="None", bld="None"):
    append("/etc/security/limits.conf", 'appmgr        hard    nofile  64000', use_sudo="True")
    append("/etc/security/limits.conf", 'appmgr        soft    nofile  64000', use_sudo="True")
    
    setpkg(ver, bld)
    tmppath=sendrpms("zama_gp", "segProc", ver, bld, rh="5") 

    with settings(warn_only=True):
        sudo("rpm -qa | grep segment | xargs rpm -e")
        sudo("TFSM_USER=appmgr TFSM_GROUP=appmgr rpm -Uvh --replacepkgs  --prefix=%s %s/*.rpm" % (amhome, tmppath))
        sudo("chown appmgr: %s/zama_gp" %amhome)
        sudo("chown -R appmgr: %s/zama_gp/segment_processing" %amhome)


@roles("segPApi")
def installSegProcApi(ver='None', bld='None'):
    reqs= [
          'oracle-instantclient11.2-basic-11.2.0.2.0',
          'python2.7-2.7.1-1oasgp',
          '3party_python-2.7.1-1oasgp',
          'mod_wsgi_python-2.7.1-1oasgp',
          ]
    ans=prompt("prep for LookAlike API (web Services)?", default="y")
    append("/root/.bash_profile", 'export ORACLE_HOME=/usr/lib/oracle/11.2/client64', use_sudo="True")
    append("/root/.bash_profile", 'export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH', use_sudo="True")

    if ans is 'y':
        sudo("yum -y install httpd")
        with cd("/tmp/"):
            put("gps_reqs.tar.gz", "/tmp/")
            run("tar -xvzf /tmp/gps_reqs.tar.gz")
            with settings(warn_only=True):
               for i in reqs:
                  rslt=sudo("rpm -qa | grep %s" %i).return_code
                  if rslt is 0:
                      print(blue("%s present" %i))
                  else:
                      print(red("%s missing, installing?" %i))
                      sudo("yum -y  --nogpgcheck localinstall /tmp/gps_req/%s*.rpm" %i)
        setpkg(ver, bld)
        tmppath=sendrpms("zama_gp", "segPApi", ver, bld, "5") 
        with settings(warn_only=True):
            sudo("TFSM_USER=appmgr TFSM_GROUP=appmgr rpm -Uvh --replacepkgs  --prefix=%s %s/*.rpm" % (amhome, tmppath))
            sudo("chown -R appmgr: /var/home/appmgr/zama_gp/*")
#            sudo("/bin/sh /var/home/appmgr/zama_gp/segment_processing/webservice/configure.sh", user="appmgr")

    else:
         print(red("nothing else to do "))


@roles("TargAd")
def installTargAd(ver='None', bld='None'):
    setpkg(ver, bld)
    tmppath=sendrpms("zama_targad","targAd", ver, bld, rh="5") 
    #stopGPS()
    with settings(warn_only=True):
       sudo("TFSM_USER=appmgr TFSM_GROUP=appmgr rpm -Uvh --replacepkgs  --prefix=%s/TargAd/ %s/*.rpm" % (amhome, tmppath))


def installGPS(ver='None', bld='None'):
    prep4GPS()
    setpkg(ver, bld)
    tmppath=sendrpms("gps","gps", ver, bld, rh="5") 
    #stopGPS()
    with settings(warn_only=True):
       sudo("TFSM_USER=appmgr TFSM_GROUP=appmgr rpm -Uvh --replacepkgs  --prefix=%s %s/*.rpm" % (amhome, tmppath))

def initializeGPS():
   sudo("/var/home/appmgr/gps/gps sub_cal_events /var/home/appmgr/gps/calendars/calevents.xml", user="appmgr")


def prep4GPS():
    reqs= [
        'python2.7-2.7.1-1oasgp',
        '3party_python-2.7.1-1oasgp',
        'oracle-instantclient11.2-basic-11.2.0.2.0'
        ]
    append("/var/home/appmgr/.bash_profile", 'export ORACLE_HOME=/usr/lib/oracle/11.2/client64', use_sudo="True")
    append("/var/home/appmgr/.bash_profile", 'export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH', use_sudo="True")

    with cd("/tmp/"):
        put("gps_reqs.tar.gz", "/tmp/")
        run("tar -xvzf /tmp/gps_reqs.tar.gz")
    with settings(warn_only=True):
        for i in reqs:
           rslt=sudo("rpm -qa | grep %s" %i).return_code
           if rslt is 0:
               print(blue("%s present" %i))
           else:
               print(red("%s missing, installing?" %i))
               sudo("yum -y --nogpgcheck localinstall /tmp/gps_req/%s*.rpm" %i)


def installGPSApi(ver='None', bld='None'):
    reqs= [
          'mod_wsgi_python-2.7.1-1oasgp',
          ]
    ans=prompt("prep for GPS API (web Services)?", default="y")
    append("/root/.bash_profile", 'export ORACLE_HOME=/usr/lib/oracle/11.2/client64', use_sudo="True")
    append("/root/.bash_profile", 'export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH', use_sudo="True")
    if ans is 'y':
        installGPS(ver, bld)
        sudo("yum -y install httpd")
        with cd("/tmp/"):
            put("gps_reqs.tar.gz", "/tmp/")
            run("tar -xvzf /tmp/gps_reqs.tar.gz")
            with settings(warn_only=True):
               for i in reqs:
                  rslt=sudo("rpm -qa | grep %s" %i).return_code
                  if rslt is 0:
                      print(blue("%s present" %i))
                  else:
                      print(red("%s missing, installing?" %i))
                      sudo("yum -y  --nogpgcheck localinstall /tmp/gps_req/%s*.rpm" %i)
    else:
         print(red("nothing else to do "))
  
def putTns():
    put("tnsnames.ora", "/tmp/")
    sudo("mkdir -p /usr/lib/oracle/11.2/client64/network/admin")
    sudo("cp /tmp/tnsnames.ora /usr/lib/oracle/11.2/client64/network/admin/.tnsnames.ora")


def fixEnv():
    append("/root/.bash_profile", 'export ORACLE_HOME=/usr/lib/oracle/11.2/client64', use_sudo="True")
    append("/root/.bash_profile", 'export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH', use_sudo="True")


def stopGPS():
    with cd("/var/home/appmgr/gps"):
        sudo("nohup ./gpsd stop", user="appmgr")
        sudo("ps aux | grep appmgr")

def stopBSD():
    with cd("/var/home/appmgr/gps"):
        sudo("nohup ./bsd stop", user="appmgr")
        sudo("ps aux | grep appmgr")

def startGPS():
    with cd("/var/home/appmgr/gps"):
        sudo("nohup ./gpsd restart", user="appmgr")
        sudo("ps aux | grep appmgr")

def startBSD():
    sudo("echo $hostname")
    with cd("/var/home/appmgr/gps"):
        sudo("nohup /var/home/appmgr/gps/bsd restart", user="appmgr")
        sudo("ps aux | grep appmgr")
#        print("return code", e)

def syncLgcConf():
   tmppath="/tmp/lgc_confs_pk"
   svn_co()
   sudo("rm -rf %s" %tmppath)
   run("mkdir -p %s" %tmppath)
   put("dev/config/lgc/%s/lgc_zama_topology.xml" % env.e, "%s" %tmppath)
   sudo("cp %s/lgc_zama_topology.xml %s/lgc/conf/" %(tmppath, amhome), user="appmgr")
   sudo("rm -rf %s" %tmppath)
   local("rm -rf dev/")



def svn_co():
    local("rm -rf dev")
    local("svn co svn://172.16.16.21/TFSM/zama_ops/main/dev")

