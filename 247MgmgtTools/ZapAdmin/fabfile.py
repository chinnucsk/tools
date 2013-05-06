import sys
import os
import datetime
#import tarfile
from time import sleep
from fabric import decorators
from fabric.colors import *
from fabric.api import *
from fabric.contrib.files import exists, sed, append
from fabric.decorators import hosts

#import shell
env.config_file = 'config.yaml'
env.user = 'pkatsovich'
env.dcash = 'dc.ash.247realmedia.com'
env.dcams = 'dc.ams.247realmedia.com'
amhome = '/var/home/appmgr'

sys.path.append(os.path.abspath('..'))
from common import *

lpconfs = [
	     "/var/home/appmgr/tfsm/zeus/conf/lp/appcfg_DB_UPLOAD.xml",
             "/var/home/appmgr/tfsm/zeus/conf/lp/appcfg_MAPPING.xml"
            ]


migrtconfs = [
 	      "/var/home/appmgr/tfsm/mr/conf/scheduler/cfg_scheduler_controller.xml",
              "/var/home/appmgr/tfsm/mr/conf/scheduler/cfg_scheduler_agent.xml",
              "/var/home/appmgr/tfsm/mr/conf/scheduler/mr-hibernate.properties",
              "/var/home/appmgr/tfsm/zeus/bluekai/metadata_upload/conf/ETL_configuration.properties"
             ]
 

collmapconfs = [
		 "/var/home/appmgr/tfsm/zeus/conf/user-segments/loader.conf",
		 "/var/home/appmgr/tfsm/zeus/conf/user-segments/mapper.conf"
             ]


migirisconfs = [
                 "/var/home/appmgr/tfsm/zeus/conf/db/appcfg_attribution.xml",
                 "/var/home/appmgr/tfsm/zeus/conf/db/replication.conf",
                 "/opt/tomcat/webapps/zeus-util/META-INF/context.xml"
               ]

migiris2confs = [
                 "/var/home/appmgr/tfsm/zeus/conf/hibernate.properties"
	        ]
dartoasconfs = [
                 "/var/home/appmgr/tfsm/zeus/conf/hibernate.properties"
	        ]

mediamindconfs = [
                  "/var/home/appmgr/tfsm/zeus/conf/hibernate.properties"
   	         ]

zaptoolsconfs = [
                  "/var/home/appmgr/tfsm/zeus/conf/atlas-tools-ui/atlas_tools/local_settings.py"
	        ]


zapadminconfs = [
		"/var/home/appmgr/tfsm/zeus/conf/management-ui/zeus/local_settings.py",
		"/var/home/appmgr/tfsm/zeus/conf/reporting-ui/database-config-ds.xml"
               ]

migzrptconfs =  [
                 "/var/home/appmgr/tfsm/zeus/conf/reporting-ui/database-config-ds.xml"
		]

rexzriconfs = [
                "/var/home/appmgr/tfsm/mr/conf/legacy/oas/rf_module.properties",
                "/var/home/appmgr/tfsm/mr/conf/webservices/mr-hibernate.properties",
                "/var/home/appmgr/tfsm/mr/conf/scheduler/cfg_scheduler_agent.xml",
                "/var/home/appmgr/tfsm/mr/conf/modules/modules.properties",
		"/var/home/appmgr/tfsm/zri/conf/load_reporting_module.properties",
		"/var/home/appmgr/tfsm/zri/conf/b3_email_reporting_module.properties",
		"/var/home/appmgr/tfsm/zri/conf/xls_create_config.xml",
		"/var/home/appmgr/tfsm/zri/conf/b3_load_primary_module.properties",
		"/var/home/appmgr/tfsm/zri/conf/b3_extract_reporting_module.properties",
		"/var/home/appmgr/tfsm/zri/conf/atlas_extract_primary_module.properties",
	        "/var/home/appmgr/tfsm/zri/conf/extract_reporting_agg_module.properties",
                "/var/home/appmgr/tfsm/zri/conf/oas_extract_reporting_module.properties",
                "/var/home/appmgr/tfsm/zri/conf/atlas_extract_reporting_module.properties",
                "/var/home/appmgr/tfsm/zri/conf/b3_extract_primary_module.properties",
                "/var/home/appmgr/tfsm/zri/conf/webservices/mr-hibernate.properties",
                "/var/home/appmgr/tfsm/zri/conf/dfa_extract_primary_module.properties",
                "/var/home/appmgr/tfsm/zri/conf/dfa_extract_reporting_module.properties",
                "/var/home/appmgr/tfsm/zri/conf/load_primary_module.properties",
                "/var/home/appmgr/tfsm/zri/conf/oas_extract_primary_module.properties",
                "/var/home/appmgr/tfsm/zri/conf/zri_replicator_module.properties"
               ]


migutilconfs = [
		"/var/home/appmgr/tfsm/mr/conf/scheduler/mr-hibernate.properties",
		"/var/home/appmgr/tfsm/mr/conf/scheduler/cfg_scheduler_controller.xml",
		"/var/home/appmgr/tfsm/zri/conf/cfg_zri_scheduler.xml"
               ]

rexuiconfs = [
                "/var/home/appmgr/tfsm/mr/conf/ui/scheduler_ui/settings.py",
		"/var/home/appmgr/tfsm/zri/conf/ui/zri/local_settings.py"
	     ]


zeusapiconfs = [
		"/opt/tomcat/webapps/zeus-api/META-INF/context.xml"
	       ]

def qa2():
 env.e = "qa"
 env. amhome = '/var/home/appmgr/tfsm'
 env.tomcathome= '/opt/tomcat'
 env.dbhost = 'ztdb-qa-scan.dc.ash.247realmedia.com'
 env.oldhost = '10.65.47.212'
 
 env.db = 'S10ZEUS'
 env.olddb = 'S4ZEUS1'
 

 env.con_str= '@(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = ztdb-qa-scan)(PORT = 1521))(CONNECT_DATA = (SERVER = DEDICATED)(SERVICE_NAME = S10ZEUS)))'
 env.old_str= '@10.65.47.212:1521:s4zeus1'
 
env.roledefs = {
             'lp' :   [
                         'logproc1-qa2',
                         'logproc2-qa2',
                         'logproc3-qa2',
                         'logproc4-qa2'
                      ],

           'migrt' :  [
                         'migrt5-qa2'
                      ],

         'collmap' :  [
                         'coll-mapper-qa2'
                      ],

         'migiris' :  [
                         'migiris1-qa2'
                      ],

        'migiris2' :  [
                         'migiris2-qa2'
                      ],

         'dartoas' :  [
                         'dart-oas-qa2'
                      ],

       'mediamind' :  [
                         'mediamind-qa2'
                      ],
  
        'zaptools' :  [
                         'zaptools1us1-qa2'
                      ],
    
        'zapadmin' :  [
                         'zapadmin1-qa2'
                      ],
      
         'migzrpt' :  [
                         'mig-zrpt1-qa2'
                      ],
      	
	 'rexzri' :  [
                         'migrt3-qa2'
                      ],

         'migutil' :  [
                         'migutil2-qa2'
                      ],
   
           'rexui' :  [
                         'migui2-qa2'
                      ],

	  'zeusapi' : [
                         'zapwebsvc1us1-qa2'
                      ],

              }


def prod():
 env.e = "prod"
 env.amhome = '/var/home/appmgr/tfsm/'
 env.dbhost = "db1011-scan"
 env.db = "P1ZEUS"
 env.tomcathome= '/opt/tomcat'

 env.oldhost = "10.65.60.71"
 env.olddb = "P1ZEUS2"

 env.con_str= "@(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = db1011-scan)(PORT = 1521))(CONNECT_DATA = (SERVER = DEDICATED)(SERVICE_NAME = P1ZEUS)))"
 env.old_str= "@10.65.60.71:1521:p1zeus2"

 env.roledefs = {
          'trackers' :   [
                         'tracker1',
                         'tracker2',
                         'tracker3',
                         'tracker4',
                         'tracker5',
                         'tracker6',
                         'tracker7',
                         'tracker8',
                         'tracker9',
                         'tracker10',
                         'tracker11',
                         'tracker12'
                      ],
   
          'lp' :   [
                         'logproc1-ash',
                         'logproc2-ash',
                         'logproc3-ash',
                         'logproc4-ash',
                         'logproc5-ash',
                         'logproc6-ash'
                      ],

           'migrt' :  [
                         'migrt5'
                      ],

         'collmap' :  [
                         'coll-mapper'
                      ],

         'migiris' :  [
                         'migiris1us2'
                      ],

        'migiris2' :  [
                         'migiris2us2'
                      ],

         'dartoas' :  [
                         'dart-oas'
                      ],

       'mediamind' :  [
                         'mediamind'
                      ],
  
        'zaptools' :  [
                         'zaptools1us1'
                      ],
    
        'zapadmin' :  [
			 'zapadmin1us1',
                         'zapadmin2us1'
                      ],
      
         'migzrpt' :  [
                         'mig-zrpt1',
                         'mig-zrpt2'
                      ],
      	
	 'rexzri' :  [
                         'migrt3',
                         'migrt4'
                      ],

         'migutil' :  [
                         'migutil2'
                      ],
   
           'rexui' :  [
                         'migui2',
                         'migui3'
                      ],

	  'zeusapi' : [
                         'zapwebsvc1us2'
                      ],

              }



def cmd():
    shell.shell()



@roles('zeusapi')
def creates4conf():
   myrole=getrole()
   roleconfs="%sconfs" % myrole

   for conf in eval(roleconfs):
       s4conf="%s.s4zeus" %conf
       s10conf="%s.s10zeus" %conf
       if not exists(s4conf):
          sudo("cp %s %s" %(conf, s4conf), user="appmgr")
          sed("%s" % s4conf, "%s" %env.con_str, "%s" %env.old_str, use_sudo=True)
          sed("%s" % s4conf, "SERVICE_NAME", "SID", use_sudo=True)
          sed("%s" % s4conf, "%s" %env.dbhost, "%s" %env.oldhost, use_sudo=True)
          sed("%s" % s4conf, "%s" %env.db, "%s" %env.olddb, use_sudo=True)
          sudo("chown appmgr: %s" % s4conf)


@roles('lp', 'migrt', 'collmap', 'migiris', 'migiris2', 'dartoas', 'mediamind', 'zaptools', 'zapadmin', 'migzrpt', 'rexzri', 'migutil', 'rexui', 'zeusapi')
def createNewConf():
   now = datetime.datetime.now()
   myrole=getrole()
   print myrole
   print "Action Timestamp :%s " %now.strftime("%Y-%m-%d-%H:%M") 
   roleconfs="%sconfs" % myrole
 
  
   for conf in eval(roleconfs):
       oldconf="%s.%s.pk" %(conf, env.olddb)
       newconf="%s.%s.pk" %(conf, env.db)

       if exists(conf):
          if not exists(oldconf):
                 print(blue("%s conf doesnt exist, creating" %oldconf))
                 sudo("cp %s %s"%(conf, oldconf), user="appmgr")
          else:
                 print(red("FILE ALREADY EXISTS!"))
          if not exists(newconf):
                 print(blue("%s conf doesn't exist, creating" %newconf))
                 sudo("cp %s %s" %(conf, newconf), user="appmgr")
                 sed("%s" % newconf, env.old_str, env.con_str, flags="i", use_sudo=True)
                 sed("%s" % newconf, env.oldhost, env.dbhost, flags="i", use_sudo=True)
                 sed("%s" % newconf, env.olddb,  env.db, flags="i", use_sudo=True)
                 sed("%s" % newconf, "SID", "SERVICE_NAME", flags="i", use_sudo=True)
       		 sed("%s" % newconf, ".DECIDEINTERACTIVE.COM", "", flags="i", use_sudo=True)
          else:
                 print(red("FILE ALREADY EXISTS!"))




@roles("lp", "migrt", "collmap", "migiris", "migiris2", "dartoas", "mediamind", "zaptools", "zapadmin", "migzrpt", "rexzri", "migutil", "rexui", "zeusapi")
def putnewconf():
   now = datetime.datetime.now()
   cur = "%s-conf-" %env.host_string + now.strftime("%Y-%m-%d-%H:%M") 
   
   myrole=getrole()
   print myrole
   print "Action Timestamp %s:" %cur
   roleconfs="%sconfs" % myrole

   for conf in eval(roleconfs):
       oldconf="%s.%s.pk" %(conf, env.olddb)
       newconf="%s.%s.pk" %(conf, env.db)

       if exists(conf):
          if not exists(oldconf):
                 print(blue("%s conf doesnt exist, creating" %oldconf))
                 sudo("cp %s %s"%(conf, oldconf), user="appmgr")
 	  else:
                 print(red("BACKUP FILE ALREADY EXISTS!"))
                 with settings(warn_only=True):
		   diff = sudo("diff %s %s" %(conf, oldconf))
                 if diff.failed:
                    print(red("Backup and current not the Same FREAK!"))

          if exists(newconf) and exists(oldconf):
             print(green("%s conf exists" %newconf))
             with settings(warn_only=True):
                diff = sudo("diff %s %s" %(conf, newconf))
                print(yellow(diff))
             if diff.failed:
                print "%s conf different from current, swapping" %newconf
                sudo("cp %s %s" %(newconf, conf), user="appmgr")
             else:
                print(green("files the same, not overwriting"))
          else:
               print(red("%s is missing!!!" %newconf))
       else:
           print(red("that config might not be for this server"))




@roles("lp", "migrt", "collmap", "migiris", "migiris2", "dartoas", "mediamind", "zaptools", "zapadmin", "migzrpt", "rexzri", "migutil", "rexui", "zeusapi")
def puts4conf():
   now = datetime.datetime.now()
   cur = "%s-conf-" %env.host_string + now.strftime("%Y-%m-%d-%H:%M") 
   sudo("mkdir /tmp/%s" %cur)
   
   myrole=getrole()
   print myrole
   print "Action Timestamp %s:" %cur
   roleconfs="%sconfs" % myrole
   for conf in eval(roleconfs):
      s4conf="%s.s4zeus" %conf
      s10conf="%s.s10zeus" %conf
      if exists(conf):
         sudo("cp %s /tmp/%s/" %(conf, cur))
         if exists("%s" %s4conf):
            print(blue("%s conf exists, making current" %s4conf))
            sudo("cp %s %s" %(s4conf, conf), user="appmgr")
         else:
            print(red("we're missing the backup!!!"))




@roles('zeusapi')
def zeusApiUp(ver='None',bld='None'):
  if ver is None or bld is None:
    print "You need to provide a version and build"
    print ver
    print bld
    sys.exit(0)
  else:
     tmppath=sendrpms("mig", ver, bld)
     with settings(warn_only = "True"):
       sudo("/etc/init.d/tomcat stop")
       sudo("rpm -Uvh %s/*.rpm" %tmppath)
       sudo("rm %s/webapps/zeus-api/WEB-INF/lib/ojdbc14.jar" %env.tomcathome)
       sudo("ln -s %s/zeus/api/lib/ojdbc6.jar %s/webapps/zeus-api/WEB-INF/lib/" %(env.amhome, env.tomcathome),user="appmgr")
       sudo("/etc/init.d/tomcat start")


@roles('migiris')
def zeusWebSvcUp(ver='None',bld='None'):
  if ver is None or bld is None:
    print "You need to provide a version and build"
    print ver
    print bld
    sys.exit(0)
  else:
     tmppath=sendrpms("mig", ver, bld)
     with settings(warn_only = "True"):
       sudo("/etc/init.d/tomcat stop")
       sudo("rpm -Uvh --force %s/*.rpm" %tmppath)
       sudo("rm %s/webapps/zeus-util/WEB-INF/lib/ojdbc14.jar" %env.tomcathome)
       sudo("ln -s %s/zeus/webservices/lib/ojdbc6.jar %s/webapps/zeus-util/WEB-INF/lib/" %(env.amhome, env.tomcathome),user="appmgr")
       sudo("/etc/init.d/tomcat start")    
     


@roles('rexzri')
def schedApiUp(ver='None',bld='None'):
  if ver is None or bld is None:
    print "You need to provide a version and build"
    print ver
    print bld
    sys.exit(0)
  else:
     tmppath=sendrpms("mig_reporting", ver, bld)
     with settings(warn_only = "True"):
       sudo("/etc/init.d/tomcat stop")
       sudo("rpm -Uvh %s/*.rpm" %tmppath)
       sudo("rm %s/webapps/zeus-util/axis2-mr/WEB-INF/lib/ojdbc14.jar" %env.tomcathome)
       sudo("ln -s %s/mr/scheduler/lib/ojdbc6.jar %s/webapps/axis2-mr/WEB-INF/lib/" %(env.amhome, env.tomcathome), user="appmgr")
       sudo("ln -s %s/mr/scheduler/lib/ojdbc6.jar %s/webapps/axis2-zeus-mr/WEB-INF/lib/" %(env.amhome, env.tomcathome), user="appmgr")
       sudo("/etc/init.d/tomcat start")    

     


@roles('migrt', 'collmap', 'migiris', 'migiris2', 'dartoas', 'mediamind', 'zaptools', 'zapadmin', 'migzrpt', 'rexzri', 'migutil', 'rexui', 'zeusapi')
def checkconf():
   myrole=getrole()
   print myrole
   roleconfs="%sconfs" % myrole
   for conf in eval(roleconfs):
     oldconf="%s.%s.pk" %(conf, env.olddb)
     newconf="%s.%s.pk" %(conf, env.db)
     if exists(conf):
        run("cat %s" %newconf)


@roles('lp', 'migrt', 'collmap', 'migiris', 'migiris2', 'dartoas', 'mediamind', 'zaptools', 'zapadmin', 'migzrpt', 'rexzri', 'migutil', 'rexui', 'zeusapi')
def checkHostname():
  run("/bin/hostname")
  run("/bin/df")
  run("/usr/bin/host autofs-ash")



@roles('trackers')
def putCrossdomain():
   put("crossdomain.xml", "/tmp/")
   sudo("cp /tmp/crossdomain.xml /var/home/appmgr/tfsm/zeus/www/html/", user="appmgr")

