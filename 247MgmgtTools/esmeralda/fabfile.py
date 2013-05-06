import sys
import os
#import tarfile
from time import sleep
from fabric import decorators
from fabric.api import *
from fabric.contrib.files import exists, sed, append
from fabric.decorators import hosts
from setenv import *

#import shell
env.config_file = 'config.yaml'
#env.user = 'pkatsovich'
env.dcash = 'dc.ash.247realmedia.com'
env.dcams = 'dc.ams.247realmedia.com'
amhome = '/var/home/appmgr/'

sys.path.append(os.path.abspath('..'))
from common import *





def installTools(ver="None",bld="None"):
  with settings(warn_only=True):
    setpkg(ver,bld)
    tmppath=sendrpms("esmeralda", "esmtools", ver, bld, "5")
    with settings(warn_only = True):
     sudo("rpm -Uvh --force %s/*.rpm" %(tmppath))

@roles('rtx')
#@parallel
def installRTX(ver="None", bld="None"):
   

  with settings(warn_only=True):
    sudo("rm -rf /tmp/esmeralda*")
#    installtbb()
#    installLgc()
#    installcorosync()
    setpkg(ver,bld)
    tmppath=sendrpms("esmeralda", "rtx", ver, bld, "5")
    with settings(warn_only = True):
     stopStCol()
     stopEngine()
#     sudo("rpm -qa | grep esm | xargs rpm -e")
     sudo("rpm -Uvh --force %s/*.rpm" %(tmppath))
     append("/etc/init.d/esm_engine.author", "export ESM_ENGINE_CONF=/var/home/appmgr/tfsm/esmeralda/rtx/config/esm_engine.conf", use_sudo=True)
     append("/etc/init.d/esm_engine.author", "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/var/home/appmgr/tfsm/esmeralda/deps/curl", use_sudo=True)
     append("/etc/init.d/esm_stat_collector.author", "export ESM_STAT_COLLECTOR_CONF=/var/home/appmgr/tfsm/esmeralda/stat_collector/config/esm_stat_collector.conf", use_sudo=True)
     startStCol()
     startEngine()



@roles('esmlp')
def installLP(ver="None", bld="None"):
 if ver is None or bld is None:
    print "You need to provide a version and build"
    print ver
    print bld
    sys.exit(0)
 else:
    setpkg(ver,bld)
#   installLgc()
    installtbb
    tmppath=sendrpms("esmeralda", "esmlp", ver, bld, "5")
    with cd("/var/home/appmgr/"):
         run("touch /tmp/install.cfg")
         append("/tmp/install.cfg", "TFSM_USER=appmgr")
         append("/tmp/install.cfg", "TFSM_GROUP=appmgr")
         sudo("cp /tmp/install.cfg ./", user="appmgr")
         run("rm /tmp/install.cfg")
    sudo("rpm -Uvh --force --nodeps --prefix=%s %s/*.rpm" %(amhome, tmppath))



@roles('esmlpmemc')
def installLpMemc(ver="None", bld="None"):
 if ver is None or bld is None:
    print "You need to provide a version and build"
    print ver
    print bld
    sys.exit(0)
 else:
    setpkg(ver,bld)
    installLgc()
    tmppath=sendrpms("esmeralda", "esmlpmemc", ver, bld, "5")
    put("/mnt/builder/3rdParty/memcached/server/1.4.5/64/memcached-1.4.5.x86_64.rpm", "/tmp/")
    sudo("rpm -Uvh /tmp/memcached-1.4.5.x86_64.rpm")
    with cd("/var/home/appmgr/"):
         run("touch /tmp/install.cfg")
         append("/tmp/install.cfg", "TFSM_USER=appmgr")
         append("/tmp/install.cfg", "TFSM_GROUP=appmgr")
         sudo("cp /tmp/install.cfg ./", user="appmgr")
         run("rm /tmp/install.cfg")
         sudo("rpm -Uvh --force --nodeps --prefix=%s %s/*.rpm" %(amhome, tmppath))



@roles('rtx', 'esmlp', 'esmlgc')
def configLgc():
 
 sudo("mkdir -p /var/home/appmgr/lgc/work/", user="appmgr")
 local("svn co svn://172.16.16.21/TFSM/esmeralda/conf/%s" %(env.e))
 if "rtx" in env.host:
     put("./%s/lgc/lgc_esm_topology.xml" %(env.e) , "/tmp/")
     put("./%s/lgc/lgcd_esm@%s.xml" %( env.e, env.host), "/tmp/")
     sudo("cp /tmp/lgc_esm_topology.xml  /var/home/appmgr/lgc/conf/", user="appmgr")
     sudo("cp /tmp/lgcd_esm@%s.xml /var/home/appmgr/lgc/conf/" %env.host, user="appmgr")
     sudo("cp /tmp/lgcd_esm@%s.xml /var/home/appmgr/lgc/conf/" %env.host, user="appmgr")
 elif "lgc" in env.host:
     put("./%s/lgc/lgc_esm_topology.xml" %(env.e) , "/tmp/")
     put("./%s/lgc/lgc_esm_de_topology.xml" %(env.e) , "/tmp/")
     put("./%s/lgc/lgc_esm@%s.xml" %( env.e, env.host), "/tmp/" )
     put("./%s/lgc/lgc_esm_de@%s.xml" %( env.e, env.host), "/tmp/" )
     put("./%s/lgc/lgcd_esm@%s.xml" %( env.e, env.host), "/tmp/" )
     sudo("cp /tmp/lgc_esm_de_topology.xml  /var/home/appmgr/lgc/conf/", user="appmgr")
     sudo("cp /tmp/lgc_esm_topology.xml  /var/home/appmgr/lgc/conf/", user="appmgr")
     sudo("cp /tmp/lgc_esm@%s.xml /var/home/appmgr/lgc/conf/" %env.host, user="appmgr")
     sudo("cp /tmp/lgc_esm_de@%s.xml /var/home/appmgr/lgc/conf/" %env.host, user="appmgr")
     sudo("cp /tmp/lgcd_esm@%s.xml /var/home/appmgr/lgc/conf/" %env.host, user="appmgr")
 elif "esmlp" in env.host:
     put("./%s/lgc/lgc_esm_topology.xml" %(env.e) , "/tmp/")
     put("./%s/lgc/lgc_esm@%s.xml" %( env.e, env.host), "/tmp/" )
     sudo("cp /tmp/lgc_esm_topology.xml  /var/home/appmgr/lgc/conf/", user="appmgr")
     sudo("cp /tmp/lgc_esm@%s.xml /var/home/appmgr/lgc/conf/" %env.host, user="appmgr")



@roles('esmlp')
def startLP():
     with cd("%s/esmeralda/bin" %amhome):
        with settings(warn_only="True"):
          sudo("nohup ./scan_control.sh start esm", user="appmgr")
          sudo("nohup ./lp.sh start parser", user="appmgr")
          sudo("nohup ./lp.sh start resolver", user="appmgr")
          sudo("nohup ./lp.sh start delayed_resolver", user="appmgr")
          sudo("nohup ./lp.sh start aggregator", user="appmgr")
          sudo("nohup ./loader_control.sh start", user="appmgr")
          sudo("ps -fu appmgr")


@roles('esmlp')
def stopLP():
     with cd("%s/esmeralda/bin" %amhome):
        with settings(warn_only="True"):
          sudo("nohup ./scan_control.sh stop esm", user="appmgr")
          sudo("nohup ./lp.sh stop parser", user="appmgr")
          sudo("nohup ./lp.sh stop resolver", user="appmgr")
          sudo("nohup ./lp.sh stop delayed_resolver", user="appmgr")
          sudo("nohup ./lp.sh stop aggregator", user="appmgr")
          sudo("nohup ./loader_control.sh stop", user="appmgr")
          sudo("ps -fu appmgr")

    


@roles('rtx')
def restartRTX():
    stopStCol()
    startStCol()
    stopEngine()
    startEngine()
    

#@roles('rtx')
def startEngine():
     sudo("/etc/init.d/esm_engine start")
     sudo("ps -fu appmgr")

#@roles('rtx')
def startStCol():
     sudo("/etc/init.d/esm_stat_collector start")
     sudo("ps -fu appmgr")


@roles('rtx')
def stopStCol():
     sudo("/etc/init.d/esm_stat_collector stop")
     sudo("ps -fu appmgr")

@roles('rtx')
def stopEngine():
     sudo("/etc/init.d/esm_engine stop")
     sudo("ps -fu appmgr")

@roles('rtx')
def startCorosync():
    sudo("/etc/init.d/corosync restart")


@roles('rtx', 'esmlp', 'esmlgc')
def quickFix():
   with settings(warn_only = True):
     put("/tmp/appmgr_bash_profile", "/tmp/appmgr_bash_profile")
     sudo("cat /tmp/appmgr_bash_profile")
     sudo("cp /tmp/appmgr_bash_profile /var/home/appmgr/.bash_profile", user="appmgr")

def NRPE():
   sudo("/etc/init.d/nrpe restart")
