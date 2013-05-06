import boto  #install from pip
import socket
import time
from boto import ec2, s3
from time import sleep
from fabric.api import *
from fabric.colors import *
from fabric.contrib.files import *
from awslib import *
from pynsca import NSCANotifier

env.user = 'ubuntu'
env.key_filename="~/.ssh/ops-east.pem"
env.keepalive=60


@task
def verifyDBRestore(app=None, pod=None):
  '''Verify if a week old mysql DB backup can be restored. Requires to supply application name'''
  if app == "production_mysql" and  pod == "sc":
    ##check if instance running, mail possible verification in progress
    region = "us-west-1"
    nagios = "monitor.sc.recurly.net"
    host = getInstance(region, tName='DBRecoveryTest')
  elif app == "production_mysql" and  pod == "ny3":
    region = "us-east-1"
    nagios = "monitor.sc.recurly.net"
    host = getInstance(region, tName='NY3DBVerify')
  else:
    print "did you provide an app who's DB to verify?" 
    print "Like production_mysql"
    sys.exit(3)
  
  print region
  if host.state != "running":
    print "Instance not running, restarting to clear ephemeral"
    startInstance(host.id, region)
  else:
    print "Instance still running, for now we'll do nothing, just restart and continue as normal"
    stopInstance(host.id, region)
    startInstance(host.id, region)
  
  env.host_string = getHostString(host.id, region)
  print env.host_string

  sleep(45)
  sudo("echo started: %s > /var/run/backup_verify" %date.today())
  dlfname = bldBkupFname(app, pod)
  dlfpath = getS3BkupFile(dlfname, '/mnt/')
  rstrpath = unpack(app, dlfpath, pod)
  restore(rstrpath)
  sleep(10)
 
  rslt = None
  cnt = 0
  while rslt == None and cnt < 6:
    rslt = prodQueries()
    sleep (20)
    cnt = cnt +1 
  
  notif = NSCANotifier(nagios)
  if rslt != None:
    graph("mysql.sc.backup_verify.recurly_production.subscriptions",  rslt )
    graph("mysql.sc.backup_verify.status", "10")
    notif.svc_result("BackupVerify", "MySQL_Prod_verify", pynsca.OK, "Subscription count: %s" %rslt)
  else:
    graph("mysql.sc.backup_verify.status", "1")  
    notif.svc_result("BackupVerify", "MySQL_Prod_verify", pynsca.WARNING, "Subscription count: %s" %rslt)

  #stopInstance(host.id, region)
  sys.exit(0)


def unpack(app, dlfpath, pod):
  '''Decrypt and un-tar backup file'''
  if 'production' in app:
    ##Decrypt if prod##
    with settings(warn_only=True):
      sudo("service mysql stop")
      sudo("rm -rf /var/lib/mysql/*")
      try:
        if 'gpg' in dlfpath:
          print(red("!!!WARNING ENCRYPTED ARCHIVE!!!"))
          sudo('HOME=/root gpg --no-use-agent --passphrase-file /root/.gpgpw  --output %s --decrypt %s'  %((dlfpath.rstrip('.gpg')), dlfpath))
          dlfpath=dlfpath.rstrip('.gpg')
        if 'bz2' in dlfpath:
          sudo("tar -C /mnt -xjvf %s" %(dlfpath))
          f = dlfpath.split(".", 3)
          rstrpath=".".join([f[0],f[1]])
          return rstrpath
        elif 'gz' in dlfpath:
          sudo("tar -C /mnt -xzvf %s" %(dlfpath))
          f = dlfpath.split(".", 3)
          rstrpath=".".join([f[0],f[1]])
          return rstrpath
        else:
          print "Unknown archive type"
      except:
        print "Something went wrong with unpacking"
        sys.exit(1)
  elif 'marketing' in dlfpath:  
    sudo("tar -C /mnt -xjvf %s" %(dlfpath))
    rstrpath='/mnt/'+(today - timedelta(days=3)).strftime("%Y-%m-%d")
    return rstrpath
  else:
    print "Unknown app"



def restore(rstrpath='None'):
  '''restore backup using innobackupex'''
  if rstrpath is not 'None':
    with settings(warn_only=True):
      sudo("service mysql stop")
      sudo("rm -rf /var/lib/mysql/*")
      try:
        sudo("innobackupex --copy-back %s" %rstrpath)
      except:
        print "Innobackupex restore failed"
        sys.exit(2)
      sudo("chown -R mysql:mysql /var/lib/mysql/")
      sudo("service mysql start")


def prodQueries():
  try:
    subs = sudo("HOME=/root/ mysql -u root -e 'select count(*) from recurly_production.subscriptions\G' | grep count | awk '{print $2}' ").stdout
    return subs.strip()
  except:
    print "something failed w/ query"
    return None
 
@task
def prepDBRecoveryHost():
  '''Install Apps required to test DB recovery''' 
  sudo("gpg --keyserver  hkp://keys.gnupg.net --recv-keys 1C4CBDCDCD2EFD2A")
  append("/etc/apt/sources.list", "deb http://repo.percona.com/apt precise main", use_sudo=True)
  append("/etc/apt/sources.list", "deb-src http://repo.percona.com/apt precise main", use_sudo=True)
  sudo("apt-get update")
  clean()
  with settings(warn_only=True):
    rslt = sudo("apt-cache search xtrabackup mysql-server mysql-server-5.5 mysql-server-core-5.5 mysql-common")
    if rslt.succeeded:
       sudo("apt-get install xtrabackup -y --force-yes")
       sudo("echo mysql-server mysql-server/root_password select t3mp0rary | debconf-set-selections")
       sudo("echo mysql-server mysql-server/root_password_again select t3mp0rary | debconf-set-selections")
       sudo("apt-get install mysql-server mysql-server-5.5 mysql-server-core-5.5 mysql-common percona-xtrabackup -y --force-yes")
       sudo("service mysql stop")
       put("./db_restore_my.cnf", "/tmp/")
       sudo("mv /tmp/db_restore_my.cnf /etc/mysql/my.cnf")
       put("./gnupg.tar.gz", "/tmp/")
       sudo("mv /tmp/gnupg.tar.gz /root/")
       sudo("tar -xvzf /root/gnupg.tar.gz -C /root")
       sudo("chown -R root:root /root/.gnupg/")


def clean():
  with settings(warn_only=True):
    sudo("service mysql stop")
    sudo("apt-get purge mysql-server mysql-server-5.5 mysql-server-core-5.5 mysql-common -y")
    sudo("rm -rf /var/lib/mysql/*; rm -rf /etc/mysql")


def bldBkupFname(app='None', pod='None'):
  '''return string of the file name we're trying to restore'''
  today = date.today()
  weekago = (today - timedelta(days=13)).strftime("%Y-%m-%d")
  if app == 'web-marketing':
    fname = '%s-%s.tar.bz2' %(app, weekago)
    return fname
  elif app == 'production_mysql':
    fname =  '%s.%s.%s.tar.bz2.gpg' %(app, pod, weekago)  
    return fname
  else:
    print "unknown app"
    return 'none'


def graph(metric_path, value):
  CARBON_SERVER = '10.138.7.53'
  CARBON_PORT = 2003

  message = '%s %s %d\n' %(metric_path, value, int(time.time()))

  print 'sending message:\n%s' % message
  sock = socket.socket()
  sock.connect((CARBON_SERVER, CARBON_PORT))
  sock.sendall(message)
  sock.close()
