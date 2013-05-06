import os
import datetime
import sys
import tarfile
from time import sleep
from fabric.api import *
from setenv import *


env.config_file = 'config.yaml'
#env.user = 'pkatsovich'
env.dcash = 'dc.ash.247realmedia.com'
amhome = '/var/home/appmgr'

    
sys.path.append(os.path.abspath('..'))
from common import *



def prepConf():
   append("/var/home/appmgr/ZapTraderUI/cfg/RTB/app.properties", "template.path=/var/home/appmgr/ZapTraderUI/templates", use_sudo=True)
   append("/var/home/appmgr/ZapTraderUI/cfg/RTB/app.properties", "facebook.flag.enabled=yes", use_sudo=True)
   append("/var/home/appmgr/ZapTraderUI/cfg/RTB/app.properties", "facebookCreative.verification.bidder.url=http://172.21.174.111/api?ex=14", use_sudo=True)
   append("/var/home/appmgr/ZapTraderUI/cfg/RTB/app.properties", "facebookCreative.imageRegEx=.+\.(?i)(jpg|jpeg|png|gif)$", use_sudo=True)
   append("/var/home/appmgr/ZapTraderUI/cfg/RTB/app.properties", "facebookCreative.imagePath=/var/home/appmgr/ZapTraderUI/creative", use_sudo=True)




@roles('ztui')
def upgradeUI(sprint='None', ver='None'):

  if sprint and ver is not 'None':
    sudo("echo DOWN > /var/home/appmgr/ZapTraderFlex/status.txt")
    run("cat /var/home/appmgr/ZapTraderFlex/status.txt")
    fnam="ZapTraderUI_%s_%s.tgz" %(sprint, ver)
    local("scp appmgr@rtbui1us2-dev1:/var/home/appmgr/NewUIRelease/build/%s /tmp/" %(fnam))
    sudo("rm -rf /tmp/%s" % fnam)
    run("mkdir -p /tmp/%s" % fnam)
    put("/tmp/%s" %fnam, "/tmp/%s/" % fnam)
    ans=stopTomcat()
    if ans == "1":
      sudo("rm -rf /opt/tomcat/webapps/ROOT/", user="appmgr")
      sudo("rm -rf /opt/tomcat/work/Catalina/", user="appmgr")
      with cd("%s" %amhome):
        sudo("cp /tmp/%s/%s ./" %(fnam, fnam), user="appmgr")
        sudo("tar -xvzf %s" %fnam, user="appmgr")
        sudo("ln -sf /var/home/appmgr/ZapTraderUI/webapps/PROD/ZAPTrader.war /opt/tomcat/webapps/ROOT.war", user="appmgr")
#      startTomcat()
    else:
     print(blue("your probably forgot to specify a version and build"))
     

@roles('ztui')
def upgradeFLEX(sprint='None', ver='None'):

    if sprint or ver is not 'None':
        fnam="ZapTraderFlex_%s_%s.tgz" %(sprint, ver)
        local("scp appmgr@rtbui1us2-dev1:/var/home/appmgr/NewUIRelease/build/%s /tmp/" %(fnam))
        run("mkdir -p /tmp/%s" % fnam)
        put("/tmp/%s" %fnam, "/tmp/%s/" % fnam)
    
        with cd("%s" %amhome):
          with settings(warn_only='True'):
            sudo("cp /tmp/%s/%s ./" %(fnam, fnam), user="appmgr")
            sudo("tar -xvzf %s" %fnam, user="appmgr")
            sudo("cp /var/home/appmgr/ZapTraderFlex/FlexDashboard_11_0_2/config.xml /var/home/appmgr/ZapTraderFlex/FlexDashboard/", user="appmgr")
     
#        stopApache()
#        startApache()



@roles('api')
def fixAPIDBConf():

   now = datetime.datetime.now()
   cur = "LPDBconf-" + now.strftime("%Y-%m-%d-%H:%M")
   run("mkdir /tmp/%s" %cur)
     
   for conf in apidbconfs:
       sudo("cp %s /tmp/%s/" %(conf, cur))
       sed("%s" % conf, "zap-scan", "db1011-scan", use_sudo=True)
       sed("%s" % conf, "10.73.60.214", "db1011-scan.dc.ash.247realmedia.com", use_sudo=True)
       sed("%s" % conf, "10.73.60.213", "db1011-scan.dc.ash.247realmedia.com", use_sudo=True)
       sed("%s" % conf, "P1ZAPLP.DECIDEINTERACTIVE.COM", "P1ZAPLP", use_sudo=True)
       sudo("chown appmgr: %s" % conf)


def syncZTUIConf():
       put("/home/pkatsovich/deploy_tools/UI/%s-ZT_UI_confs.tgz" %env.e, "/tmp/")
       sudo("cp /tmp/%s-ZT_UI_confs.tgz %s" %(env.e, amhome))
       with cd("%s" %amhome):
           sudo("tar -xvzf %s-ZT_UI_confs.tgz" %env.e, user="appmgr")
       sudo("mkdir -p %s/ZapTraderFlex/cfg/RTB/" %amhome, user="appmgr")
       sudo("mkdir -p %s/ZapTraderUI/cfg/RTB/" %amhome, user="appmgr")

       sudo("cp %s/%s-ZT_UI_confs/config.xml %s/ZapTraderFlex/FlexDashboard/config.xml" %(amhome, env.e, amhome), user="appmgr")
       sudo("cp %s/%s-ZT_UI_confs/hibernate.properties %s/ZapTraderUI/cfg/hibernate.properties" %(amhome, env.e, amhome), user="appmgr")
       sudo("cp %s/%s-ZT_UI_confs/log4j.xml_ztui %s/ZapTraderUI/cfg/log4j.xml" %(amhome, env.e, amhome), user="appmgr")
       sudo("cp %s/%s-ZT_UI_confs/mail.properties %s/ZapTraderUI/cfg/mail.properties" %(amhome, env.e, amhome), user="appmgr")
       sudo("cp %s/%s-ZT_UI_confs/app.properties %s/ZapTraderUI/cfg/RTB/app.properties" %(amhome, env.e, amhome), user="appmgr")
       sudo("cp %s/%s-ZT_UI_confs/db.properties %s/ZapTraderUI/cfg/RTB/db.properties" %(amhome, env.e, amhome), user="appmgr")
       sudo("cp %s/%s-ZT_UI_confs/dashboard-api.properties %s/tfsm/zama/conf/dashboard-api/dashboard-api.properties" %(amhome, env.e, amhome), user="appmgr")
       sudo("cp %s/%s-ZT_UI_confs/log4j.xml_dash %s/tfsm/zama/conf/dashboard-api/log4j.xml" %(amhome, env.e, amhome), user="appmgr")
       sudo("cp %s/%s-ZT_UI_confs/databaseconf.properties %s/tfsm/zama/notifications_manager/conf/" %(amhome, env.e, amhome), user="appmgr")
       
       sudo("rm %s/%s-ZT_UI_confs.tgz" %(amhome, env.e))
       run(" rm /tmp/%s-ZT_UI_confs.tgz" %env.e)

