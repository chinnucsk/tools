import os
import sys
import boto
import datetime
from datetime import date, timedelta 
from boto import ec2, s3
from time import sleep
from fabric.api import *
from credentials import *


#env.user = 'ubuntu'
#env.key_filename="~/.ssh/ops.pem"

@task
def getAvailInstances(region):
  '''Return all instance ID's, Name by Tag, status and how to connect by region (default: us-west-1)'''
  try:
    #conn = ec2.connect_to_region(region)
    conn = ec2.connect_to_region(region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
    res = conn.get_all_instances()
  except: 
    regions = ec2.regions()
    print "select a region: %s" %regions
  
  for r in res:
    for i in r.instances:
      tag = 'None'
      if "Name" in i.tags:
        tag = i.tags['Name']
      
      if i.public_dns_name:
        print 'UID: {0:15} State: {1:15} Tag: {2:25} SSH To: {3}'.format(i.id, i.state, tag, i.public_dns_name)
      elif i.private_ip_address:
        print 'UID: {0:15} State: {1:15} Tag: {2:25} SSH To: {3}'.format(i.id, i.state, tag, i.private_ip_address)
      else:
        print 'UID: {0:15} State: {1:15} Tag: {2:25} SSH To: {3}'.format(i.id, i.state, tag, i.ip_address)


def getInstance(region='None', uid='None', tName='None'):
  
  #ec2 = boto.ec2.connect_to_region('us-west-1')
  try: 
    #conn = ec2.connect_to_region(region)
    conn = ec2.connect_to_region(region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
  except:
    regions = ec2.regions()
    print "FAIL, did you provide region? %s" %regions
 
  ##Get instance by UID
  res = conn.get_all_instances()
  if uid is not 'None':
    for r in res:
      for i in r.instances:
        if uid == i.id:
          return i
  ##get instance by Tag Name
  elif tName is not 'None':
    for r in res:
      for i in r.instances:
        if "Name" in i.tags:
           tag = i.tags['Name']
           if tag == tName:
             return i
  else:
    print "Instance not found"
    return None


from fabric.api import *
from fabric.colors import green as _green, yellow as _yellow
import boto
import boto.ec2
from config import *
import time
 
def create_server():
    """
    Creates EC2 Instance
    """
    print(_green("Started..."))
    print(_yellow("...Creating EC2 instance..."))
    
 
    image = conn.get_all_images(ec2_amis)
 
    reservation = image[0].run(1, 1, key_name=ec2_key_pair, security_groups=ec2_security,
        instance_type=ec2_instancetype)
 
    instance = reservation.instances[0]
    conn.create_tags([instance.id], {"Name":config['INSTANCE_NAME_TAG']})
    while instance.state == u'pending':
        print(_yellow("Instance state: %s" % instance.state))
        time.sleep(10)
        instance.update()
 
    print(_green("Instance state: %s" % instance.state))
    print(_green("Public dns: %s" % instance.public_dns_name))
 
    return instance.public_dns_name

@task
def startInstance(id='None', region='None'):
  '''start the AWS instance, supply id, i.e: fab startInstance:i-0000000  get uid from fab getAvailInstances'''
  if getInstance(region, id):
    i = getInstance(region, id)
    if i.state == "stopped":
      print "Instance currently not running, starting"
      i.start()
      getAvailInstances(region)
    while i.state != "running":
      i = getInstance(region, id)
      print i.state
      sleep(5)
  else:
    print "Instance specified DNE, try again:"
    getAvailInstances(region)


@task
def stopInstance(id='None', region='None'):
  '''stop the AWS instance, supply id, i.e: fab stopInstance:i-0000000  get uid from fab etAvailInstances'''
  if getInstance(region, id):
    i = getInstance(region, id)
    if i.state == "running":
      print "Instance currently running, stopping"
      i.stop()
      getAvailInstances(region)
      while i.state != "stopped":
        i = getInstance(region, id)
        print i.state
        sleep(5)
  else:
    print "Instance specified DNE, try again:"
    getAvailInstances(region)


def getHostString(id='None', region='None'):
  if getInstance(region, id):
    i = getInstance(region, id)
  else:
    print "Host not found, did you suply a valid UID from the list below?"
    getAvailInstances(region)
  if i.public_dns_name:
    hostString = i.public_dns_name
  elif i.private_ip_address:
    hostString =  i.private_ip_address
    print hostString
  else:
    print "can't find where to connect, exiting"
    hostString = 'None'
    exit(1)  
  return hostString
  



def getS3BkupFile(dlfname='None', dlpath='/mnt/'):
  if dlfname is not None:
    print dlfname
    fpath = "mysql/%s" %(dlfname)
    print fpath
    url = getS3URL('recurly-backups', fpath)
    print 
    with cd("%s" %dlpath):
      dlfpath = "%s%s" %(dlpath, dlfname)
      sudo("rm -rf %s" %(dlfpath))
      try: 
        sudo("curl -o %s '%s'" %(dlfpath, url))
        return dlfpath
      except:
        print "Something went wrong downloading the file"
        sys.exit(1)


def getS3URL(bucket='None', fname='None'):
  if bucket and fname is not None:
    try:  
     # conn = boto.connect_s3()
      from boto.s3.connection import S3Connection
      conn = S3Connection(aws_id, aws_key)
      bucket = conn.get_bucket(bucket)
      key = bucket.get_key(fname)
      S3url = key.generate_url(36000)
      return S3url
    except:
      print  "Backup file not found %s%s" %(bucket, fname)
      sys.exit(1)

