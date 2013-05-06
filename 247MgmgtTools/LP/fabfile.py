import os
import datetime
import tarfile
import socket
import sys
from time import sleep
from fabric.api import *
from fabric.contrib.files import *
env.config_file = 'config.yaml'
env.dcash = 'dc.ash.247realmedia.com'
amhome = '/var/home/appmgr'
from setenv import *
sys.path.append(os.path.abspath('..'))

from common import getrole, addUser, installLgc, installtbb, sendrpms, preprpm, checktbb, checklgc



lpdbconfs = [
             "/var/home/appmgr/.tnsnames.ora",
             "/var/home/appmgr/zama_gp/conf/hadoop-conf/zama.db.xml",
             "/var/home/appmgr/zama_gp/conf/conf.ini"
            ]


lpsvcs = [
          "aggregator",
          "delayed_resolver",
          "mapper",
          "parser",
          "resolver",
          "conversion_flusher",
          "loader"
         ]





@roles('lp')
def installLP(ver=None, bld=None):
##Check if LGC is installed, check if TBB is installed, install zama_lp,
# copy over configs from local, sed out line that needs to be hosts IP.
#
#

 ip=socket.gethostbyname(env.host_string)
 if ver is None or bld is None:
    print "You need to provide a version and build"
    print ver
    print bld
    sys.exit(0)
 else:
    setpkg(ver, bld)
    installtbb()
    installLgc()
    ans = prompt("Remove old lp rpm's (y/n)? ", default="N")
    tmppath=sendrpms("zama_lp", "lp", ver, bld) 
    with settings(warn_only=True):
        if ans is "y":
            sudo("rpm -qa | grep lp | xargs rpm -e ")
            sudo("rpm -Uvh --replacepkgs --prefix=%s %s/*.rpm" % (amhome, tmppath))
        elif ans is "n":
            print("stopping LP")
            sudo("rpm -Uvh --replacepkgs --prefix=%s %s/*.rpm" % (amhome, tmppath))
        else:
            print("quitting")
            sys.exit()
    sudo("rm -rf %s" %tmppath)


@roles('lpmemc')
def upgradeLPMEMC():
  '''stop MemCache and upgrade with new RPM'''
  #stopLPMEMC()
  put("../memcached-1.4.5.x86_64.rpm", "/tmp/")
  sudo("rpm -ivh /tmp/memcached-1.4.5.x86_64.rpm")
  #checkUsrProc()



def stopLPMEMC():
  '''stop LP Memcache'''
  checkUsrProc()
  sudo("/var/home/appmgr/zama/bin/memcached.sh stop", user="appmgr")
  checkUsrProc()

def startLPMEMC():
  #checkUsrProc()
  sudo("/var/home/appmgr/zama/bin/memcached.sh start", user="appmgr")
  checkUsrProc()


@roles('lp')
def upgradeLP(ver="None", bld="None"):
    setpkg(ver, bld)
    tmppath=sendrpms("zama_lp", "lp", ver, bld) 
    with settings(warn_only=True):
       sudo("rpm -Uvh --replacepkgs --prefix=%s %s/*.rpm" % (amhome, tmppath))



@roles('lp')
def zamaStopLP():
  with settings(warn_only="True"):
    sudo("/root/zama_stop.sh")
    checkUsrProc()




@roles("lp")
#@parallel
def stopLP():

#
###Multiple elements comprise(services) LP as listed in lpsvcs, they have to be brought down in a specific order
###Some use similar commands, some are more complicated.

###First we stop parser
###Then we stop 
#
  with settings(warn_only = True):
   checkUsrProc()
   with cd("/var/home/appmgr/zama/bin/"):
       for svc in lpsvcs:
           if svc is not "loader":
              print(blue("stoping %s" %svc))
              sudo("./lp.sh stop %s" % svc, user="appmgr")
           else:
              print(blue("stoping loader"))
              sudo("./loader.sh stop", user="appmgr")

  checkUsrProc()
   


@roles('lp')
def startLP():
  '''start all LP related processes ( aggregator delayed_resolver mapper parser resolver conversion_flusher)'''
  checkUsrProc()
  with cd("~appmgr/zama/bin/"):
       for svc in lpsvcs:
           if svc is not "loader":
              sudo("./lp.sh start %s" % svc, user="appmgr")
           else:
              sudo("./loader.sh start", user="appmgr")

  checkUsrProc()


def checkUsrProc(user="appmgr"):
  '''check if LP is running'''
  with settings(warn_only = True): 
   sudo("ps aux | grep  %s " % user)

def startparser():
  '''stop all parser gracefully and carefully'''

  checkUsrProc()

  with cd("~appmgr/zama/bin/"):
#
###Take down parser, force sleep 5 mins to make sure we don't break something
   with settings(warn_only = True):
       print "Starting parser"
       sudo("./lp.sh start parser")
       checkUsrProc()



def stopparser():
  '''stop all parser gracefully and carefully'''

  checkUsrProc()

  print "Stopping parser"
  sudo("./lp.sh stop parser")

  print "sleeping for 5 minutes"

  for i in range(1, 6):
    sleep(5)
    t=30-(i*5)
    print "sleeping, %ss remaining" % t

  print "Sleep done, stoping other services"

@roles('lp')
def modConf(cnf='None', txt='None'):
    '''append a line to a config file'''
    cnf="/var/home/appmgr/zama/conf/lp/appcfg.xml"
    txt=[
        '<entry name="lom.keep_expensive_wins">1</entry>',
        '<entry name="lom.expensive_wins_log_level">13</entry>'
        ]

    for t in txt: 
        with settings(warn_only="True"):
            rsl=run("grep -ir '%s' %s" %(t,cnf)).return_code      
            print(blue(rsl))
        if rsl is 1:
             print(red(t)) 
             print(red("Not present in config"))
             print(red(cnf))
             print(red("Modifying"))
             sudo("sed -i -e '42a\                  %s' %s " %(t, cnf), user="appmgr")
        else:
            print(blue(t))
            print(blue("exists in"))
            print(blue(cnf))


def stopCLCTR():
  '''stop collector'''
  with cd('%s' %amhome):
     sudo("./zama_gp/scripts/zama_gp.sh collector stop", user="appmgr")


def startCLCTR():
  '''start collector'''
  with cd('%s' %amhome):
     sudo("./zama_gp/scripts/zama_gp.sh collector start", user="appmgr")

@roles('lp')
def quickLog():
 with settings(warn_only = True):  
   run("mkdir /tmp/core_logs2")
   run("tar -cvzf /tmp/core_logs_%s.tar.gz /tmp/core_logs2/" %env.host_string) 

@roles('lp')
def stopSA():
  '''stop segment aggregator'''
  with cd('%s' %amhome):
     sudo("/var/home/appmgr/zama/bin/segment_aggregator.sh stop", user="appmgr")

#@roles('lp')
def startSA():
  '''start segment aggregator'''
  with cd('%s' %amhome):
     sudo("/var/home/appmgr/zama/bin/segment_aggregator.sh start", user="appmgr")

@roles('lp')
def stopAG():
  '''stop aggregator'''
  with cd('%s' %amhome):
     sudo("/var/home/appmgr/zama/bin/lp.sh stop aggregator", user="appmgr")

@roles('lp')
def startAG():
  '''start aggregator'''
  with cd('%s' %amhome):
     sudo("/var/home/appmgr/zama/bin/lp.sh start aggregator", user="appmgr")



def syncLgcConf():
   tmppath="/tmp/lgc_confs_pk"
   svn_co()
   sudo("rm -rf %s" %tmppath)
   run("mkdir -p %s" %tmppath)
   put("dev/config/lgc/%s/lgc_zama_topology.xml" % env.e, "%s" %tmppath)
   sudo("cp %s/lgc_zama_topology.xml %s/zama/conf/" %(tmppath, amhome), user="appmgr")
   sudo("rm -rf %s" %tmppath)

@runs_once
def svn_co():
    local("rm -rf dev")
    local("svn co svn://172.16.16.21/TFSM/zama_ops/main/dev")


