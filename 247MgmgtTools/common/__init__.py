import os
import tarfile
import re
import socket
from time import sleep
from fabric.api import *
from fabric.operations import *
from fabric.contrib.files import *
from fabric.colors import *
#amhome= '/var/home/appmgr'





def packages(app='None', ver=None, build=None):
        '''set list of rpm's for each server role'''

#        env.rpmlist = { 
#
#                      }

#
#                      'nearRT'  :   (
#                                     "zama_odps_near_rt-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
#                                   ),
#                      'readers'  :   (
#                                     "zama_odps_rtb_reader-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
#                                   ),
#		      'rtbcollectors'  :   (
#                                     "zama_odps_rtb_collector-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
#                                   ),	
#	              'oascollectors'  :   (
#                                     "zama_odps_oas_collector-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
#                                   ),
#
#		      'analytics'  :   (
#                                     "zama_odps_analytics-%s-bld%s.rh5.x86_64.rpm" %(ver, build),
#                                   ),
#
#		      'zeusapi'  :   (
#                                     "tfsm-zeus-api-%s-bld%s.rh4.x86_64.rpm" %(ver, build),
#                                   ),
#		      'migiris'  :   (
#                                     "tfsm-zeus-webservices-%s-bld%s.rh4.x86_64.rpm" %(ver, build),
#                                   ),
#		      'rexzri'  :   (
#                                     "tfsm-mr-schd-api-%s-bld%s.rh4.x86_64.rpm" %(ver, build),
#                                   ),
        
        role=getrole()
        if app in env.rpmlist.iterkeys():
            rpmlist = env.rpmlist[app]
            print rpmlist
            return rpmlist
        elif role in env.rpmlist.iterkeys():
            rpmlist = env.rpmlist[role]
            print rpmlist
            return rpmlist
        else:
           print "Can't find which rpm's to use"



def sendrpms(product=None, app=None, ver=None, build=None, rh=None):
#
##prep the rpms (make a tar.gz)
#
 if app is 'None':
        app  = getrole()
 print(" send rpms  %s" %app )
 print ("build", build)
 tmppath = "/tmp/%s%s%s" % (app, ver, build)
 tfile = "%srpms.tar.gz" % (app)
 local("mkdir -p %s/" % tmppath)
 preprpm(product, app, ver, build, rh)
#
##send the rpm's tar to the hosts
#
 run("mkdir -p %s/" % tmppath)
 put("%s/%s" %(tmppath, tfile), tmppath)
 
 with cd(tmppath):
   sudo("tar -xvzf %s -C %s" %(tfile, tmppath))
#
##Clean up local copy
#

 return tmppath



def preprpm(product=None, app=None, ver=None, build=None, rh=None):
 '''taking rpm's that are listed in env.rpmlist and tarring them up for transfer to destination hosts'''
 print ("preprpm %s" %app)
 tmppath= "/tmp/%s%s%s" % (app, ver, build)
 print rh
 buildpath=bldPath(product, ver, build, rh)
 rpms = packages(app, ver, build)

 tfile = tarfile.open("%s/%srpms.tar.gz" % (tmppath, app), 'w:gz')
 with cd(buildpath):
     for k in rpms:
        print k
        tfile.add("%s/%s" % (buildpath,k), k)
     
     for f in tfile.getnames():
        print "added %s" % f

 tfile.close()



def bldPath(product='None',ver='None',bld='None',rh='5'):
  print rh
  if None in (product, ver, bld):
    print "you need to supply each of the following: product, component, ver, bld"
    sys.exit(0)
  elif '4' in rh:
    buildpath= '/mnt/builder/shadowBuilds/%s/%s/build_%s/bin/gcc_3.4.6' %(product, ver, bld, )
  elif '5' in rh:
    buildpath= '/mnt/builder/shadowBuilds/%s/%s/build_%s/bin/gcc_4.1.2' %(product, ver, bld, )
  return buildpath

 

def getrole():
  '''returns the role of the current host'''

  for currole, hosts in env.roledefs.items():
      if env.host_string in env.roledefs[currole]:
          role = currole
          print role
          return role
      else: 
          role="None"





def addUser(who='None'):
  '''Add specified user on destination host if doesnt already exist'''
  with settings(warn_only = True):
      exists = run('id %s' % who)

      if 'appmgr' in who:
           sudo("groupmod -g 11001 %s" % who)
           sudo("usermod -g 11001 -u 11001 %s" %who )
           sudo("mkdir -p /var/home/%s" %who )
           sudo("groupadd -g 11001 %s" % who)
           sudo("useradd -g 11001 -d /var/home/%s %s" %(who, who))
           sudo("chown -R %s: /var/home/%s" %(who, who))
      else:
           sudo ("useradd -d /var/home/%s %s" %(who, who))


def checkPkg(pkg="httpd"):
  '''check if httpd is installed'''
  with settings(warn_only = True):
    exists = sudo("rpm -qa | grep %s" %pkg)
    
    if pkg in exists:
       return True
    else:
       return False


def installhttpd():
  '''insall httpd if it doesnt exist'''
  if checkPkg("httpd") is False:
     sudo("yum -y install httpd")
  else:
     print "httpd already installed"


def installTomcat():
  '''install Tomcat from own RPM'''
  if checkPkg("tomcat") is False:
     put("/home/pkatsovich/redhat/RPMS/noarch/tomcat-6.0.32-0.noarch.rpm", "/tmp")
     sudo("yum -y localinstall /tmp/tomcat-6.0.32-0.noarch.rpm --nogpgcheck")
  else:
     sudo("rpm -qa | grep tomcat")
     print "Tomcat already installed"

def stopApache():
    '''Stop Apache httpd'''

    ans = prompt("Stop Apache httpd? y/n ", default="n")
    if ans is "y":
        sudo("/etc/init.d/httpd stop")
    else:
        print "Not stoping httpd"


def startApache():
    '''Stop Apache httpd'''

    ans = prompt("Start Apache httpd? y/n ", default="n")
    if ans is "y":
        sudo("/etc/init.d/httpd start")
    else:
        print "Not starting httpd"



def stopTomcat():
    '''Stop Tomcat'''

    ans = prompt("Stop and clean Tomcat?  (1=init.d) (2=/usr/local)", default="N")
    if ans is "1":
        sudo("/etc/init.d/tomcat stop")
    elif ans is "2":
        sudo("/usr/local/tomcat/bin/shutdown.sh", user="appmgr")   
    else:
        print "Not restarting tomcat"
    return ans



def startTomcat():
    '''Actually attempt to restart Tomcat'''
    ans = prompt("Stop and clean Tomcat?  (1=init.d) (2=/usr/local)", default="N")
    if ans is "1":
        sudo("/etc/init.d/tomcat stop")
        sudo("/etc/init.d/tomcat restart")
    elif ans is "2":
        sudo("/usr/local/tomcat/bin/shutdown.sh", user="appmgr")   
        sudo("/usr/local/tomcat/bin/startup.sh", user="appmgr")   
    else:
        print "Not restarting tomcat"


   
def installcorosync():
  tbb = checkcorosync()
  if tbb is False:
      put('/mnt/builder/3rdParty/corosync/1.3.1/gcc_4.1.2/64/tfsm-corosync-gcc_4.1.2-1.3.1-1.x86_64.rpm', '/tmp/')
      sudo('rpm -ivh /tmp/tfsm-corosync-gcc_4.1.2-1.3.1-1.x86_64.rpm')
      sudo("ln -s /opt/corosync/etc/init.d/corosync /etc/init.d/corosync")
  else: 
     print "corosync already installed"


def checkcorosync():
  '''check if tbb is installed'''
  with settings(warn_only = True):
    exists = run("rpm -qa | grep tfsm-corosync")
    if 'corosync' in exists:
       return True
    else:
       return False

def installtbb():
  tbb = checktbb()
  if tbb is False:
#      put('/mnt/builder/3rdParty/tbb/3.0-20100406/gcc_4.1.2/64/tfsm-tbb-linux_gcc_cc4.1.2_libc2.5.7_kernel2.6.18-3.0-20100406.x86_64.rpm', '/tmp/')
      put('/mnt/builder/3rdParty/tbb/3.0-20100406/gcc_4.1.2/tfsm-tbb-linux_gcc_cc4.1.2_libc2.5.7_kernel2.6.18-3.0-20100406.x86_64.rpm', '/tmp/')
      sudo('rpm -ivh /tmp/tfsm-tbb-linux_gcc_cc4.1.2_libc2.5.7_kernel2.6.18-3.0-20100406.x86_64.rpm')
  else: 
     print "tbb already installed"


def checktbb():
  '''check if tbb is installed'''
  with settings(warn_only = True):
    exists = run("rpm -qa | grep tbb-linux")
    if 'tbb-linux' in exists:
       return True
    else:
       return False

def installLgc(ver,bld):
   path=bldPath("oas_lgc",ver,bld)
   addUser('appmgr')
#   lgc=checklgc()
#   if lgc is False:
   put('%s/lgc-%s-bld%s.rh5.x86_64.rpm' %(path, ver, bld), '/tmp/')
   sudo('OAS_USER=appmgr OAS_GROUP=appmgr rpm -Uvh --force --replacefiles --replacepkgs --prefix=/var/home/appmgr /tmp/lgc-%s-bld%s.rh5.x86_64.rpm' %(ver, bld))
#   else:
#      print "lgc already installed"


def installIdgen(ver='None',bld='None'):

 if ver or bld is not 'None':
      path=bldPath("Common",ver,bld)
      put('%s/tfsm-id-gen-%s-bld%s*.rpm' %(path, ver, bld), '/tmp/tfsm-id-gen-%s-bld%s*.rpm' %(ver, bld) )
      sudo('rpm -ivh  --force --replacepkgs --prefix=/var/home/appmgr/tfsm /tmp/tfsm-id-gen-%s-bld%s*.rpm' %(ver, bld) )
 else:
      print "PRovide version and build number plz"


def checklgc():
  '''check if lgc is installed'''
  with settings(warn_only = True):
    exists = run("rpm -qa | grep lgc")

    if 'lgc' in exists:
       return True
    else:
       return False





def getid():
#  id = re.search("(\d*)\D*(\d*)\D*(\d*)", env.host_string)
  id = re.search("\D*(\d*)(us\d|eu\d)", env.host_string)
  print env.host_string
  if id: 
     return id.group(1)
  else:
     print "No digits in hostname, WTF?"


def getdc():
  id = re.search("\D*(\d*)(us\d|eu\d)", env.host_string)
  print env.host_string
  if id: 
     return id.group(2)
  else:
     print "No digits in hostname, WTF?"


def parseHost():
  if '-' in env.host_string:
      id = re.search("(\D*)(\d*)(us\d|eu\d|ap\d)(-dev\d|-stg\d|-int\d|-qa\d)", env.host_string)
      return {'host':id.group(1), 'id':id.group(2), 'dc':id.group(3), 'env':id.group(4)}
  else:
      id = re.search("(\D*)(\d*)(us\d|eu\d|ap\d)", env.host_string)
      return {'host':id.group(1), 'id':id.group(2), 'dc':id.group(3), 'env':""}
     

def addPxyIP(pxy='None'):
   if pxy is not 'None':
     hst = parseHost()
     pxyfullname = 'rtb%s%s%s' % (pxy, hst['id'], hst['dc'])
     ip = socket.gethostbyname('rtb%s%s%s%s' % (pxy, hst['id'], hst['dc'], hst['env']))
     if '-' not in env.host_string: 
        print(red("Assuming PRODUCTION Using bond0 as interface"))
        print ip
    	sudo("echo DEVICE=bond0:%s" % pxy )
 	sudo("echo IPADDR=%s"  %ip )
        sudo("echo 'DEVICE=bond0:%s' > /etc/sysconfig/network-scripts/ifcfg-bond0:%s" %(pxy, pxy) )
        sudo("echo 'BOOTPROTO=static' >> /etc/sysconfig/network-scripts/ifcfg-bond0:%s" %(pxy) )
        sudo("echo 'IPADDR=%s' >> /etc/sysconfig/network-scripts/ifcfg-bond0:%s" %(ip,pxy) )
        sudo("echo 'NETMASK=255.255.255.0' >> /etc/sysconfig/network-scripts/ifcfg-bond0:%s" %(pxy) )
        sudo("echo 'ONBOOT=yes' >> /etc/sysconfig/network-scripts/ifcfg-bond0:%s" %(pxy) )
     elif 'qa' or 'stg' in env.host_string:
        print(red("Not production using eth0 as interface"))
        print ip
    	sudo("echo DEVICE=eth0:%s" % pxy )
 	sudo("echo IPADDR=%s"  %ip )
        sudo("echo 'DEVICE=eth0:%s' > /etc/sysconfig/network-scripts/ifcfg-eth0:%s" %(pxy, pxy) )
        sudo("echo 'BOOTPROTO=static' >> /etc/sysconfig/network-scripts/ifcfg-eth0:%s" %(pxy) )
        sudo("echo 'IPADDR=%s' >> /etc/sysconfig/network-scripts/ifcfg-eth0:%s" %(ip,pxy) )
        sudo("echo 'NETMASK=255.255.255.0' >> /etc/sysconfig/network-scripts/ifcfg-eth0:%s" %(pxy) )
        sudo("echo 'ONBOOT=yes' >> /etc/sysconfig/network-scripts/ifcfg-eth0:%s" %(pxy) )
   else:
     print "you probably forgot the proxy abreviation"



def checkPuppet():
  '''check if puppet is installed'''
  with settings(warn_only = True):
    exists = run("rpm -qa | grep puppet")

    if 'puppet' in exists:
       return True
    else:
       return False



def installPuppet(e='False'):
#  if not checkPuppet() and e:
     sudo("rm -rf /tmp/puppetstuff")
     run("mkdir /tmp/puppetstuff")
     #ans=prompt("Install Master? (y/n)", default='n')
     #if ans is 'y':
     #    put("/home/pkatsovich/redhat/RPMS/noarch/puppet-server-2.7.13-1.noarch.rpm", "/tmp/puppetstuff/")

     put("/home/pkatsovich/redhat/RPMS/noarch/puppet-2.7.13-1.noarch.rpm", "/tmp/puppetstuff/")
     put("/home/pkatsovich/redhat/RPMS/noarch/facter-1.5.8-1.el5.noarch.rpm", "/tmp/puppetstuff/")
     put("/home/pkatsovich/redhat/RPMS/x86_64/ruby-shadow-1.4.1-7.x86_64.rpm", "/tmp/puppetstuff/")
     with settings(warn_only = True):
          sudo("yum -y install ruby ruby-libs ruby-shadow")
          sudo("yum -y install /tmp/puppetstuff/*.rpm --nogpgcheck")
          run("rm -rf /tmp/puppetstuff")


def prepPupp(e="None"):
    if (e != 'None'):
	if not checkPuppet():
           installPuppet()
        if checkPuppet(): 
           if ("rtb_qa" in e):
              master="rtbpuppet1us2-stg1.dc.ash.247realmedia.com"
              ip = socket.gethostbyname("%s" %master)
              append("/etc/hosts", "%s %s" %(ip, master), use_sudo='True')
              sed("/etc/puppet/puppet.conf", "environment = qa", "environment = rtb_qa", use_sudo = True)
              sed("/etc/puppet/puppet.conf", "environment = mig_qa", "environment = rtb_qa", use_sudo = True)
              append("/etc/puppet/puppet.conf", "environment = rtb_qa", use_sudo = True)
              append("/etc/puppet/puppet.conf", "server = rtbpuppet1us2-stg1.dc.ash.247realmedia.com", use_sudo = True)
           elif ("esm_qa" in e):
              master="rtbpuppet1us2-stg1.dc.ash.247realmedia.com"
              ip = socket.gethostbyname("%s" %master)
              append("/etc/hosts", "%s %s" %(ip, master), use_sudo='True')
              sed("/etc/puppet/puppet.conf", "environment = qa", "environment = esm_qa", use_sudo = True)
              sed("/etc/puppet/puppet.conf", "environment = mig_qa", "environment = esm_qa", use_sudo = True)
              append("/etc/puppet/puppet.conf", "environment = esm_qa", use_sudo = True)
              append("/etc/puppet/puppet.conf", "server = rtbpuppet1us2-stg1.dc.ash.247realmedia.com", use_sudo = True)
           elif ("stg" in e) or ("staging" in e) or ("rtb_stg" in e):
              master="rtbpuppet1us2-stg1.dc.ash.247realmedia.com"
              ip = socket.gethostbyname("%s" %master)
              append("/etc/hosts", "%s %s" %(ip, master), use_sudo = True)
              sed("/etc/puppet/puppet.conf", "environment = staging", "environment = rtb_stg", use_sudo = True)
              append("/etc/puppet/puppet.conf", "environment = rtb_stg", use_sudo = True)
              append("/etc/puppet/puppet.conf", "server = rtbpuppet1us2-stg1.dc.ash.247realmedia.com", use_sudo = True)
           elif ("prod" in e) or ("mig" in e):
              print("prod")
              master="sysmgt1us2.dc.ash.247realmedia.com"
              ip = socket.gethostbyname("%s" %master)
              append("/etc/hosts", "%s %s" %(ip, master), use_sudo=True)
              sed("/etc/puppet/puppet.conf", "environment = prod", "environment = mig" )
              append("/etc/puppet/puppet.conf", "environment = mig")
              append("/etc/puppet/puppet.conf", "server = sysmgt1us2.dc.ash.247realmedia.com")
           elif "oas_qa" in e:
              append("/etc/puppet/puppet.conf", "environment = oas_qa", use_sudo = True)
              append("/etc/puppet/puppet.conf", "server = rtbpuppet1us2-stg1.dc.ash.247realmedia.com", use_sudo = True)
           else:
              print " Specify env"
        else:
              print "Specify env: i.e. fab prepPupp:qa"
          

def removePuppet():
   sudo("rpm -qa | grep puppet| xargs rpm -e")
   sudo("rm -rf /etc/puppet/")
   sudo("rm -rf /var/lib/puppet/")


def stopPupp():
    sudo("/etc/init.d/puppet stop")

def startPupp():
    sudo("/etc/init.d/puppet start")


def runPupp():
   with settings(warn_only = "True"):  
        sudo("/usr/sbin/puppetd --test")


def zStop():
    with cd("/root"):
        sudo("./zama_stop.sh")

def zStart():
    with cd("/root"):
        sudo("./zama_start.sh")



def interactive():
  open_shell()


def rhn(e='None'):
  print(e)
  if ('stg' in e) or ('qa' in e):
      append("/etc/hosts", "10.73.61.171 sat1us2 sat1us2.dc.ash.247realmedia.com", use_sudo=True)
      put("/home/pkatsovich/deploy_tools/common/mig_rtb_virthost_stg.sh", "/tmp/")
      run("chmod +x /tmp/mig_rtb_virthost_stg.sh")
      run("/tmp/mig_rtb_virthost_stg.sh")
  elif ('prod' in e):
      append("/etc/hosts", "10.73.61.171 sat1us2 sat1us2.dc.ash.247realmedia.com", use_sudo=True)
      put("/home/pkatsovich/deploy_tools/common/mig_rtb_rhel5.sh", "/tmp/")
      run("chmod +x /tmp/mig_rtb_rhel5.sh")
      run("/tmp/mig_rtb_rhel5.sh")
  else:
      print("Invalid environment specified")
      

def fixTZ(zone='None'):
  if zone is not None:
     sudo("ln -sf /usr/share/zoneinfo/%s /etc/localtime" %zone)
     sed("/etc/sysconfig/clock","ZONE=.*","", use_sudo=True)
     append('/etc/sysconfig/clock', 'ZONE="%s"' %zone, use_sudo=True)
     sudo("/etc/init.d/ntpd stop")
     sudo("/usr/sbin/ntpdate 172.21.175.15")
     sudo("/etc/init.d/ntpd restart")
  else:
     print("specify zone")

def mkhk():
    sudo("/bin/hostname %s.dc.hk.247realmedia.com" %env.host_string)

def lgcMon():
    put("/home/pkatsovich/deploy_tools/common/scripts/lgc_mon2.sh", "/tmp/")
    put("/home/pkatsovich/deploy_tools/common/scripts/.lgc_mon2.sh", "/tmp/")
    sudo("mkdir -p /var/home/appmgr/scripts/bin/", user="appmgr")
    sudo("cp /tmp/lgc_mon2.sh /var/home/appmgr/scripts/bin/", user="appmgr")
    sudo("cp /tmp/.lgc_mon2.sh /var/home/appmgr/", user="appmgr")
