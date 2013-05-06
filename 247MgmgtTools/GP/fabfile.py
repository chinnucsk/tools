import os
import datetime
import sys
import tarfile
from time import sleep
from fabric.api import *
from fabric.contrib.files import exists, sed, append

sys.path.append(os.path.abspath('..'))

from common import *


env.config_file = 'config.yaml'
env.user = 'pkatsovich'
env.dcash = 'dc.ash.247realmedia.com'
env.dcams = 'dc.ams.247realmedia.com'
env.dchk = 'dc.hk.247realmedia.com'
amhome = '/var/home/appmgr'

gpdbconfs = [
            "/var/home/appmgr/zama_gp/conf/hadoop-conf/zama.db.xml",
            "/var/home/appmgr/zama_gp/conf/conf.ini"
           ]

def stg():
 env.roledefs = {
                'hdpM' : ['rtbhdp1us2-stg1.%s' % env.dcash],
                'hdpS' : ['rtbhdp2us2-stg1.%s' % env.dcash,
                          'rtbhdp3us2-stg1.%s' % env.dcash,
                          'rtbhdp4us2-stg1.%s' % env.dcash
                         ],
                'lp'   : ['rtblp1us2-stg1.%s' % env.dcash,
                          'rtblp2us2-stg1.%s' % env.dcash,
                          'rtblp3us2-stg1.%s' % env.dcash,
                          'rtblp4us2-stg1.%s' % env.dcash
                         ],
                }

def prodams():
 env.roledefs = {
                'hdpM' : ['rtbhdp1eu1.%s' % env.dcams],
                'hdpS' : ['rtbhdp2eu1.%s' % env.dcams,
                          'rtbhdp3eu1.%s' % env.dcams,
                          'rtbhdp4eu1.%s' % env.dcams,
                          'rtbhdp5eu1.%s' % env.dcams,
                          'rtbhdp6eu1.%s' % env.dcams
                         ],
                'lp'   : ['rtblp1eu1.%s' % env.dcams,
                          'rtblp2eu1.%s' % env.dcams,
                         ],
                }


def prodhk():
 env.roledefs = {
                'hdpM' : ['rtbhdp1ap1.%s' % env.dchk],
                'hdpS' : ['rtbhdp2ap1.%s' % env.dchk,
                          'rtbhdp3ap1.%s' % env.dchk,
                          'rtbhdp4ap1.%s' % env.dchk
                         ],
                'lp'   : ['rtblp1ap1.%s' % env.dchk,
                          'rtblp2ap1.%s' % env.dchk,
                         ],
                }


def prodec():
 env.roledefs = {
                'hdpM' : ['rtbhdp5us2.%s' % env.dcash],
                'hdpS' : ['rtbhdp6us2.%s' % env.dcash,
                	  'rtbhdp7us2.%s' % env.dcash,
                          'rtbhdp8us2.%s' % env.dcash,
                          'rtbhdp9us2.%s' % env.dcash,
                          'rtbhdp10us2.%s' % env.dcash,
                          'rtbhdp11us2.%s' % env.dcash,
                          'rtbhdp12us2.%s' % env.dcash
                         ],
                'hdpLP'   : ['rtblp1us2.%s' % env.dcash,
                          'rtblp2us2.%s' % env.dcash,
                          'rtblp3us2.%s' % env.dcash,
                          'rtblp4us2.%s' % env.dcash,
                          'rtblp5us2.%s' % env.dcash,
                          'rtblp6us2.%s' % env.dcash
                         ],
                }


def qa():
 env.roledefs = {
                'lp' :      ['rtblp1us1-qa1.%s' % env.dcash,
                             'rtblp2us1-qa1.%s' % env.dcash
                            ],
                'hdpS' :    [
                                'rtbhdp2us1-qa1.%s' % env.dcash,
                                'rtbhdp3us1-qa1.%s' % env.dcash,
                                'rtbhdp4us1-qa1.%s' % env.dcash
                            ],
                'hdpM' :   ['rtbhdp1us1-qa1.%s' % env.dcash]

                }




def esmdev():
 env.roledefs = {
                'lp' :      ['esmlp1us2-dev1.%s' % env.dcash,
                             'esmlp2us2-dev1.%s' % env.dcash,
                             'esmlp3us2-dev1.%s' % env.dcash,
                             'esmlp4us2-dev1.%s' % env.dcash
                            ],
                'hdpS' :    [
                                'esmhdp2us2-dev1.%s' % env.dcash,
                                'esmhdp3us2-dev1.%s' % env.dcash,
                                'esmhdp4us2-dev1.%s' % env.dcash
                            ],
                'hdpM' :   ['esmhdp1us2-dev1.%s' % env.dcash]

                }




@roles('hdpLP')
def upHDPM(ver, bld):
#   stopHDP()
   tmppath=sendrpms("zama_gp", "hdpLP", ver, bld)
   sudo("rpm -Uvh --prefix=%s %s/*.rpm" %(amhome, tmppath) )
   mkhdpconf()


@roles('hdpS')
def upHDPS(ver, bld):
   #sudo("rpm -Uvh --prefix=%s /zama_gp__config-6.1-bld001.rh5.x86_64.rpm" % amhome)
   tmppath=sendrpms("zama_gp", "hdpS", ver, bld)
   sudo("rpm -Uvh --prefix=%s %s/*.rpm" %(amhome, tmppath))
   mkhdpconf()


@roles("hdpM")
def stopHDP():
  with cd("%s/zama_gp/scripts/" % amhome):
      sudo("./zama_gp.sh aggregator stop", user="appmgr")
      sudo("./zama_gp.sh arf stop", user="appmgr")
      sudo("./zama_gp.sh loader stop", user="appmgr")


@roles("hdpM")
def startHDP():
  with cd("%s/zama_gp/scripts/" % amhome):
      sudo("./zama_gp.sh aggregator start", user="appmgr")
      sudo("./zama_gp.sh arf start", user="appmgr")
      sudo("./zama_gp.sh loader start", user="appmgr")


def mkhdpconf():
  with cd("%s/zama_gp/conf" % amhome):
       sudo("/var/home/appmgr/zama_gp/scripts/configure.sh zama_gp")


@roles('hdpS')
def whatrole():
#   r = getrole(env.host_string, env.roles, env.roledefs)
   r = getrole()
   print r



@roles('hdpS','hdpM', 'lp')
def prephdp():
   addusr("appmgr")
#   addusr("hadoop")
#   sudo("usermod -G appmgr hadoop")
#   sudo("usermod -G hadoop appmgr")
   sudo("mkdir -p /var/home/appmgr && chown -R appmgr: /var/home/appmgr")
   sudo("mkdir -p /var/home/hadoop && chown -R hadoop: /var/home/hadoop")
   sudo("usermod -d /var/home/appmgr appmgr")
   sudo("usermod -d /var/home/hadoop hadoop")
   sudo("touch /var/home/hadoop/.bash_profile", user="hadoop")
   sudo("touch /var/home/appmgr/.bash_profile", user="appmgr")
   sudo("echo '\numask 0002' >> /var/home/hadoop/.bash_profile", user="hadoop")
   sudo("echo '\numask 0002' >> /var/home/appmgr/.bash_profile", user="appmgr")
   sudo("chmod 755 /var/home/hadoop/", user="hadoop")
   sudo("chmod 755 /var/home/appmgr/", user="appmgr")
 


@runs_once
def gethdp():
   local("wget -r -l1 'http://archive.cloudera.com/redhat/cdh/3u0/RPMS/noarch/' ")
   tfile = tarfile.open("./hadoop.tar.gz", 'w:gz')
   with cd("./archive.cloudera.com/redhat/cdh/3u0/RPMS/noarch"):
     tfile.add("./archive.cloudera.com/redhat/cdh/3u0/RPMS/noarch/")
     for f in tfile.getnames():
        print "added %s" %f



@roles('hdpS', 'hdpM', 'lp')
def puthdp():
   gethdp()
   put('./hadoop.tar.gz', '/tmp/')
   run("tar -xvzf /tmp/hadoop.tar.gz -C /tmp/")
   sudo("yum -y install redhat-lsb")
   with cd("/tmp/archive.cloudera.com/redhat/cdh/3u0/RPMS/noarch/"):
        run("mv hadoop-0.20-source-*.rpm ..")
        sudo("rpm -ivh --aid hadoop-0.20*rpm")


@roles('hdpS', 'hdpM', 'lp')
def installjdk():
    put("./jdk-6u26-linux-amd64.rpm", "/tmp/")
    sudo("rpm -ivh /tmp/jdk-6u26-linux-amd64.rpm")



#@roles('hdpS', 'hdpM', 'lp')
#def removehdp():
# with cd("/tmp/archive.cloudera.com/redhat/cdh/3b2/RPMS/noarch/"):
#   with settings (warn_only=True):
#    sudo("for i in hadoop-0.20*rpm ; do rpm -e $(echo $i | sed 's/\.rpm//g') --nodeps; done")

@roles('hdpS', 'hdpM', 'lp')
def fixusr():
    sudo('(echo ""; echo "umask 0002") >> ~mapred/.bash_profile')
    sudo('/usr/sbin/usermod -a -G appmgr mapred')
    sudo('(echo ""; echo "umask 0002") >> ~hdfs/.bash_profile')
    sudo('/usr/sbin/usermod -a -G appmgr hdfs')
    sudo('(echo ""; echo "umask 0002") >> ~appmgr/.bash_profile')
    sudo('/usr/sbin/usermod -a -G hadoop,hdfs,mapred appmgr')


@roles('hdpM', 'hdpS', 'lp')
def putLib():
    with cd("/tmp"):
        put("./commons-collections-3.2.1-bin.zip", "/tmp/")
        sudo("unzip commons-collections-3.2.1-bin.zip")
        sudo("cp commons-collections-3.2.1/commons-collections-3.2.1.jar /usr/lib/hadoop-0.20/lib/")
        sudo("rm -rf commons-collections-3.2.1 commons-collections-3.2.1.bin.zip")


@roles("hdpS")
def hdpStop():
   with cd("/var/home/appmgr/zama_gp/scripts/"):
      sudo("./hadoop_daemons.sh stop")

@roles("hdpS")
def hdpStart():
   with cd("/var/home/appmgr/zama_gp/scripts/"):
      sudo("./hadoop_daemons.sh start")


@roles("hdpLPp")
def stopCollector():
   sudo("/var/home/appmgr/zama_gp/scripts/zama_gp.sh collector stop", user="appmgr")

@roles("hdpLP")
def startCollector():
   sudo("/var/home/appmgr/zama_gp/scripts/zama_gp.sh collector start", user="appmgr")


@roles('hdpM', 'hdpS')
def fixGPDBConf():
 with settings(warn_only=True):
   now = datetime.datetime.now()
   cur = "GPDBconf-" + now.strftime("%Y-%m-%d-%H:%M")
   run("mkdir /tmp/%s" %cur)
     
   for conf in gpdbconfs:
       sudo("cp %s /tmp/%s/" %(conf, cur))
       sed("%s" % conf, "zap-scan", "db1011-scan", use_sudo="True")
       sed("%s" % conf, "10.73.60.214", "db1011-scan.dc.ash.247realmedia.com", use_sudo="True")
       sed("%s" % conf, "P1ZAPLP.DECIDEINTERACTIVE.COM", "P1ZAPLP", use_sudo="True")
       sudo("chown appmgr: %s" % conf)

@roles('hdpM', 'hdpS', 'lp')
def dbUp():
  put("zama.db.xml.new", "/tmp")
  sudo("cp /tmp/zama.db.xml.new /var/home/appmgr/zama_gp/conf/hadoop-conf/zama.db.xml", user ="appmgr")
  run("rm -f /tmp/zama.db.xml.new")


@roles('hdpM', 'hdpS', 'lp')
def dbDown():
  put("zama.db.xml.orig", "/tmp")
  sudo("cp /tmp/zama.db.xml.orig /var/home/appmgr/zama_gp/conf/hadoop-conf/zama.db.xml", user ="appmgr")
  run("rm -f /tmp/zama.db.xml.orig")


@roles('lp')
def lpdbUp():
  put("tnsnames.ora.new", "/tmp")
  sudo("cp /tmp/tnsnames.ora.new /var/home/appmgr/.tnsnames.ora", user ="appmgr")
  run("rm -f /tmp/tnsnames.ora.new")



@roles('lp')
def lpdbDown():
  put("tnsnames.ora.orig", "/tmp")
  sudo("cp /tmp/tnsnames.ora.orig /var/home/appmgr/.tnsnames.ora", user ="appmgr")
  run("rm -f /tmp/tnsnames.ora.orig")



@roles("hdpM", "hdpS")
def ulimit():
    run("cp /etc/security/limits.conf /tmp/limits.conf")
    append("/etc/security/limits.conf", "hdfs hard nofile 16384", use_sudo="True")
    append("/etc/security/limits.conf", "hdfs soft nofile 16384", use_sudo="True")
    append("/etc/security/limits.conf", "mapred hard nofile 16384", use_sudo="True")
    append("/etc/security/limits.conf", "mapred soft nofile 16384", use_sudo="True")



def quick():
   sudo("mkdir -p /hdfs_data/mapred/local")
   sudo("mkdir -p /disk1/mapred/local")
   sudo("chown -R mapred:hadoop /disk1/mapred/")
   sudo("chown -R mapred:hadoop /hdfs_data/mapred/")
