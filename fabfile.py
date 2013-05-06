import os
import datetime
import sys
import boto
import socket  
from bkup_verify import *
from fabric.api import *
from fabric.contrib.files import *
from awslib import *
from setenv import *

#env.user = 'ubuntu'
#env.key_filename="~/.ssh/ops.pem"
#setRoles("ny3")

def checkPuppet():
  '''check if puppet is installed'''
  with settings(warn_only = True):
    exists = run("dpkg -l | grep puppet")
    if 'puppet' in exists:
       return True
    else:
       return False

@task
def runPupp(e=None):
   with settings(warn_only = "True"):
        sudo("/usr/bin/puppet agent -vt --environment=%s" %e)

@task
def prepHost():
  '''add a host to puppet'''
  env.host = raw_input("Full Hostname: ")
  env.env = raw_input("environment: ")
  master="ops.sc.recurly.net"

  sudo("echo %s > /etc/hostname" % env.host)
  sudo("hostname %s" % env.host)
 
  print env.host_string
  print env.host
  if not checkPuppet():
    append("/etc/resolv.conf", "nameserver 10.128.7.4", use_sudo = True)
    append("/etc/hosts", "%s %s" %(env.host_string, env.host), use_sudo = True)
    sudo("apt-get clean")
    sudo("apt-get update")
    sudo("apt-get install puppet -y --force-yes")
    sudo("apt-get upgrade -y --force-yes")
  if checkPuppet(): 
    ip = socket.gethostbyname("%s" %master)
    sed("/etc/hosts", "126.0.0.1", "127.0.0.1", use_sudo = True)
    append("/etc/hosts", "%s %s puppet" %(ip, master), use_sudo = True)
    append("/etc/puppet/puppet.conf", "environment = %s" %(env.env), use_sudo = True)
    runPupp(env.env)
#  elif ("prod" in e) or ("mig" in e):
#    print("prod")
#    master="sysmgt1us2.dc.ash.247realmedia.com"
#    ip = socket.gethostbyname("%s" %master)
#    append("/etc/hosts", "%s %s" %(ip, master), use_sudo=True)
#    sed("/etc/puppet/puppet.conf", "environment = prod", "environment = mig" )
#    append("/etc/puppet/puppet.conf", "environment = mig")
#    append("/etc/puppet/puppet.conf", "server = sysmgt1us2.dc.ash.247realmedia.com")
  else:
    print " Specify env"

@task
def fixLocalhost():
  sed("/etc/hosts", "126.0.0.1", "127.0.0.1", use_sudo = True)
