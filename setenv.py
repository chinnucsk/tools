import sys
import os
from time import sleep
from fabric import decorators
from fabric.api import *
from fabric.contrib.files import exists, sed, append
from fabric.decorators import hosts

env.sc = 'sc.recurly.net'
env.ny = 'ny.recurly.net'
env.ny3 = 'ny3.recurly.net'
amhome = '/var/home/appmgr'

def setRoles(pod = None):
 env.e = "production"
 env.tld = '.%s.recurly.net' %pod
 env.roledefs = {
                'web' : [
                         'web1%s' %env.tld,
                         'web2%s' %env.tld
                        ],
                'lb' : [
                         'lb1%s' %env.tld,
                         'lb2%s' %env.tld
                        ],
		'trans' :     [
                               'trans1%s' %env.tld,
                               'trans2%s' %env.tld
                             ],
                'service' : [
                              'service1%s' %env.tld,
                             ],
                'redis' :    [
                              'redis1%s' %env.tld,
                             ],
                'mysql' :   [
                               'mysql1%s' %env.tld,
                               'mysql2%s' %env.tld
                             ],
  
}
