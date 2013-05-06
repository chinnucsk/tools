import os
import sys
from time import sleep
from fabric.api import *
#env.user = 'pkatsovich'
env.dcash = 'dc.ash.247realmedia.com'
amhome = '/var/home/appmgr'

sys.path.append(os.path.abspath('..'))
from common import *

def prod():
    env.roledefs = {
                   'nearRT'        :  ['rtbopt2us2.%s' % env.dcash, 'rtbopt1us2.%s' % env.dcash],
		   'readers'       :  [
                                       #'rtbopt7us2.%s' % env.dcash, 
                          	       'rtbopt8us2.%s' % env.dcash,
                                       'rtbopt9us2.%s' % env.dcash,
                                       'rtbopt10us2.%s' % env.dcash,
                                       'rtbopt11us2.%s' % env.dcash,
                                       'rtbopt12us2.%s' % env.dcash],
                   'rtbcollectors' :  ['rtbopt3us2.%s' % env.dcash,
                                       'rtbopt4us2.%s' % env.dcash],
                   'oascollectors' :  ['rtbopt5us2.%s' % env.dcash],
                   'analytics'     :  ['rtbopt6us2.%s' % env.dcash],
#                   'all'	   :  ['rtbopt1us2', 'rtbopt2us2', 'rtbopt6us2', 'rtbopt4us2', 'rtbopt5us2']

                   }
    env.e = "prod_ec"


@roles('analytics' )
def installJdk():

   with settings(warn_only = True):
     exists = run("rpm -qa | grep jdk")
    
     if 'jdk' in exists:
        print "jdk installed"
     else:
 #       put("./jdk-6u25-linux-amd64.rpm", "/tmp/")
        sudo("rpm -ivh /home/pkatsovich/jdk-6u25-linux-amd64.rpm")




@roles('nearRT', 'readers', 'collectors', 'analyzers' )
def installJboss():
   sudo("mkdir -p /opt/jboss-5.1.0.GA/", user="appmgr")
   sudo("unzip /home/pkatsovich/jboss/jboss-5.1.0.GA.zip -d /opt/", user="appmgr")
   sudo("cp /home/pkatsovich/run.conf /opt/jboss-5.1.0.GA/bin/run.conf", user="appmgr")
   sudo("cp /home/pkatsovich/jboss_init_redhat.sh /opt/jboss-5.1.0.GA/bin/", user="appmgr")


@roles('nearRT', 'readers', 'collectors', 'analyzers' )
def putLibs():
   buildpath="/mnt/builder/3rdParty/java"
   run("mkdir -p /tmp/odps-reqs")
   put("%s/apache-commons/lang/2.5/commons-lang-2.5.jar" %buildpath, "/tmp/odps-reqs/")
   put("%s/apache-commons/pool/1.5.5/commons-pool-1.5.5.jar" %buildpath, "/tmp/odps-reqs/")
   put("%s/log4j/1.2.15/log4j-1.2.15.jar" %buildpath, "/tmp/odps-reqs/")
   
   with cd("/opt/jboss-5.1.0.GA/server/default/lib"):
          sudo("cp /tmp/odps-reqs/*.jar ./")
          
   sudo("mkdir -p /etc/ld.so.conf.d")
   sudo("touch /etc/ld.so.conf.d/oracle_11_2_client.conf")
   sudo("echo '/usr/lib/oracle/11.2/client64/lib/' > /etc/ld.so.conf.d/oracle_11_2_client.conf")



@roles('nearRT', 'collectors', 'analyzers', 'analytics', 'readers')
def installOraClient():
   buildpath="/mnt/builder/3rdParty/db/oracle/11.2.0.2/"
   run("mkdir -p /tmp/odps-reqs")
   put("%s/oracle-instantclient11.2-basic-11.2.0.2.0.x86_64.rpm" %buildpath, "/tmp/odps-reqs/")
   with settings(warn_only="True"):
     sudo("rpm -ivh /tmp/odps-reqs/oracle*.rpm")


@roles('nearRT', 'collectors', 'analyzers', 'readers')
def prepOjdbc():
   sudo("cp /usr/lib/oracle/11.2/client64/lib/ojdbc6.jar /opt/jboss-5.1.0.GA/server/default/lib/", user="appmgr")
   put("/tmp/mysql-connector-java-5.1.16-bin.jar", "/tmp/odps-reqs/")
   sudo("cp /tmp/odps-reqs/mysql-connector-java-5.1.16-bin.jar /opt/jboss-5.1.0.GA/server/default/lib/", user="appmgr")



@roles('collectors', 'analyzers', 'analytics')
def prepMysql():
    put("/tmp/MySQL-server-5.1.57-1.glibc23.x86_64.rpm", "/tmp/odps-reqs/")
    put("/tmp/MySQL-client-5.1.57-1.glibc23.x86_64.rpm", "/tmp/odps-reqs/")
    with settings(warn_only="True"):
      sudo("rpm -ivh /tmp/odps-reqs/MySQL*.rpm")
      sudo("cp /usr/share/mysql/my-huge.cnf /etc/my.cnf")
    

@roles('collectors', 'analyzers', 'analytics')
def makeLogDirs():
   sudo("mkdir -p /var/home/appmgr/rtb_odps/logs", user="appmgr")


@roles('nearRT', 'readers')
def makeLgcDirs():
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/reader/in/rtb", user="appmgr")
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/reader/work/rtb", user="appmgr")
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/reader/in/oas", user="appmgr")
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/reader/work/oas", user="appmgr")
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/reader/in/zeus", user="appmgr")
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/reader/work/zeus", user="appmgr")



@roles('nearRT', 'collectors')
def makeOutDirs():
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/collector/out", user="appmgr")


@roles('collectors')
def makeArchDirs():
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/collector/work/rtb", user="appmgr")
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/collector/archive/rtb", user="appmgr")


@roles('analyzers')
def makeAOutDirs():
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/analyzer/out", user="appmgr")

@roles('analytics')
def makeAInDirs():
   sudo("mkdir -p /var/home/appmgr/rtb_odps/work/analyzer/in", user="appmgr")
 	  				 	 	 	   	 	  	   		  	 
@roles('nearRT', 'collectors', 'analyzers', 'analytics', 'readers')
def Lgc():
   installLgc()

@roles('nearRT', 'collectors', 'analyzers', 'analytics', 'readers')
def mkdir():
    sudo("mkdir -p /var/home/appmgr/zama/bin", user="appmgr")



def installODPS(ver='None', bld='None'):
   installRT(ver,bld)
   installReaders(ver,bld)
   installCollectors(ver,bld)
   installAnalyzers(ver,bld)


@roles('nearRT')
def installRT(ver='None', bld='None'):
    tmppath=sendrpms("zama_odps", ver, bld)
    sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh stop")
    sudo("ps aux | grep java")
    ans = prompt('All java dead? continue?', default="y")
    if ans is 'y' or 'Y':
       sudo("ps -ef | grep appmgr")

       while ans is not "n":
         ans = prompt('If any appmgr process to kill, enter PID', default="n")
         if ans.isdigit():
            sudo("kill -9 %s" %ans)
         else:
            print "Please enter a PID (number) or 'n' to continue"
       sudo("ps -ef | grep appmgr")
       sudo("ps -ef | grep java")
       ans = prompt("OK to install RPM's?", default="n")
       if ans is "y" or "Y":
           with cd("%s" %tmppath):
             svn_co()
             put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath)
             sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh rpm --prefix=%s -Uvh  %s/*.rpm" %(tmppath, env.e, amhome, tmppath))
             print("starting appmgr scripts")
             sudo("nohup /var/home/appmgr/zama/bin/rtb_logs_2_odps_reader.sh&", user="appmgr")
             sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh start")
       else:
           print "quitting"
           sys.exit(1)


@roles('rtbcollectors')
def installRTBC(ver='None', bld='None'):
    tmppath=sendrpms("zama_odps", ver, bld)
#    sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh stop")
    sudo("ps aux | grep java")
    ans = prompt('All java dead? continue?', default="y")
    if ans is 'y' or 'Y':
       sudo("ps -ef | grep appmgr")

       while ans is not "n":
         ans = prompt('If any appmgr process to kill, enter PID', default="n")
         if ans.isdigit():
            sudo("kill -9 %s" %ans)
         else:
            print "Please enter a PID (number) or 'n' to continue"
       sudo("ps -ef | grep appmgr")
       sudo("ps -ef | grep java")
       ans = prompt("OK to install RPM's?", default="n")
       if ans is "y" or "Y":
           with cd("%s" %tmppath):
              svn_co()
              put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath)
              sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh rpm --prefix=%s -Uvh  %s/*.rpm" %(tmppath, env.e,  amhome, tmppath))
              print("starting appmgr scripts")
              sudo("nohup /var/home/appmgr/zama/bin/rtb_data_2_odps_collector.sh &", user="appmgr")
              sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh start")
       else:
           print "quitting"
           sys.exit(1)

@roles('oascollectors')
def installOASC(ver='None', bld='None'):
    tmppath=sendrpms("zama_odps", ver, bld)
#    sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh stop")
    sudo("ps aux | grep java")
    ans = prompt('All java dead? continue?', default="y")
    if ans is 'y' or 'Y':
       sudo("ps -ef | grep appmgr")

       while ans is not "n":
         ans = prompt('If any appmgr process to kill, enter PID', default="n")
         if ans.isdigit():
            sudo("kill -9 %s" %ans)
         else:
            print "Please enter a PID (number) or 'n' to continue"
       sudo("ps -ef | grep appmgr")
       sudo("ps -ef | grep java")
       ans = prompt("OK to install RPM's?", default="n")
       if ans is "y" or "Y":
           with cd("%s" %tmppath):
              svn_co()
              put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath)
              sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh rpm --prefix=%s -Uvh  %s/*.rpm" %(tmppath, env.e, amhome, tmppath))
              print("starting appmgr scripts")
#             sudo("/var/home/appmgr/zama/bin/create_oas_collector_table.sh", user="appmgr")
              sudo("nohup /var/home/appmgr/zama/bin/oas_logs_2_odps_reader.sh&", user="appmgr")
              sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh start")
              sudo("ps -ef | grep appmgr")
              sudo("ps -ef | grep java")

       else:
           print "quitting"
           sys.exit(1)


@roles('analytics')
def installAnalytics(ver='None', bld='None'):
    tmppath=sendrpms("zama_odps", ver, bld)
#    sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh stop")
    sudo("ps aux | grep java")
    ans = prompt('All java dead? continue?', default="y")

    if ans is 'y' or 'Y':
       sudo("ps -ef | grep appmgr")

       while ans is not "n":
         ans = prompt('If any appmgr process to kill, enter PID', default="n")
         if ans.isdigit():
            sudo("kill -9 %s" %ans)
         else:
            print "Please enter a PID (number) or 'n' to continue"
 
       sudo("ps -ef | grep appmgr")
       sudo("ps -ef | grep java")
       ans = prompt("OK to install RPM's?", default="n")

       if ans is "y" or "Y":
           with cd("%s" %tmppath):
             svn_co()
             put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath)
             sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh rpm --prefix=%s -Uvh  %s/*.rpm" %(tmppath, env.e, amhome, tmppath))
           print("starting appmgr scripts")
           sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh start")
           sudo("nohup /var/home/appmgr/zama/bin/rtb_data_2_odps_mapper.sh&", user="appmgr", pty=False)
           sudo("nohup /var/home/appmgr/zama/bin/odps_analyzer_data_2_mapper.sh&", user="appmgr", pty=False)
       else:
           print "quitting"
           sys.exit(1)


@roles('readers')
def installReaders(ver='None', bld='None'):
    tmppath=sendrpms("zama_odps", ver, bld)
#    sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh stop")
    sudo("ps aux | grep java")
    ans = prompt('All java dead? continue?', default="y")
    if ans is 'y' or 'Y':
       sudo("ps -ef | grep appmgr")

       while ans is not "n":
         ans = prompt('If any appmgr process to kill, enter PID', default="n")
         if ans.isdigit():
            sudo("kill -9 %s" %ans)
         else:
            print "Please enter a PID (number) or 'n' to continue"
       sudo("ps -ef | grep appmgr")
       sudo("ps -ef | grep java")
       ans = prompt("OK to install RPM's?", default="n")
       if ans is "y" or "Y":
           with cd("%s" %tmppath):
             svn_co()
             put("dev/config/environments/env_%s.sh" % env.e, "%s" %tmppath)
             sudo("TFSM_TOPOLOGY_DEFINED=/%s/env_%s.sh rpm --prefix=%s -Uvh  %s/*.rpm" %(tmppath, env.e,  amhome, tmppath))
           print("starting appmgr scripts")
           sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh start")
           sudo("nohup /var/home/appmgr/zama/bin/rtb_logs_2_odps_reader.sh >& /dev/null < /dev/null &", user="appmgr")
           sudo("ps -ef | grep appmgr")
       else:
           print "quitting"
           sys.exit(1)




@roles('nearRT', 'readers', 'collectors')
def quickFix():
    sudo("cp /tmp/com.tfsm.*.jar  /opt/jboss-5.1.0.GA/server/default/lib/", user="appmgr")
    sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh restart")


#@roles('nearRT', 'readers', 'oascollectors', 'oascollectors', 'analytics', )
def stopJBOSS():
    print "stopping jboss"
    sudo("/opt/jboss-5.1.0.GA/bin/jboss_init_redhat.sh stop")
    sudo("ps -ef | grep java")
    sudo("ps -ef | grep jboss")


def checkJava():
    sudo("ps -ef | grep java")

def svn_co():
    local("rm -rf dev")
    local("svn co svn://172.16.16.21/TFSM/zama_ops/main/dev")

def onetime():
    sudo("nohup /var/home/appmgr/zama/bin/odps_analyzer_data_2_mapper.sh >&/dev/null &", user="appmgr")
