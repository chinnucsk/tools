#! /usr/bin/python
import urllib
import sys

dcash = "dc.ash.247realmedia.com"
roledefs = {
            'rtbbid' :  [
                        'rtbbid1us2.%s' % dcash,
                        'rtbbid2us2.%s' % dcash,
                        'rtbbid3us2.%s' % dcash,
                        'rtbbid4us2.%s' % dcash,
                        'rtbbid5us2.%s' % dcash,
                        'rtbbid6us2.%s' % dcash,
                        'rtbbid7us2.%s' % dcash,
                        'rtbbid8us2.%s' % dcash,
                        'rtbbid9us2.%s' % dcash,
                        'rtbbid10us2.%s' % dcash,
                        'rtbbid11us2.%s' % dcash,
                        'rtbbid12us2.%s' % dcash,
                        'rtbbid13us2.%s' % dcash,
                        'rtbbid14us2.%s' % dcash,
                        'rtbbid15us2.%s' % dcash,
                        'rtbbid16us2.%s' % dcash,
                        'rtbbid17us2.%s' % dcash,
                        'rtbbid18us2.%s' % dcash,
                        'rtbbid19us2.%s' % dcash,
                        'rtbbid20us2.%s' % dcash
                        ],
            'rtbmatch' :  [
                        'rtbbid1us2.%s' % dcash,
                        'rtbbid2us2.%s' % dcash,
                        'rtbbid3us2.%s' % dcash,
                        'rtbbid4us2.%s' % dcash,
                        'rtbbid5us2.%s' % dcash,
                        'rtbbid6us2.%s' % dcash,
                        'rtbbid7us2.%s' % dcash,
                        'rtbbid8us2.%s' % dcash
                        ],
            'rtbfbx' :  [
                        'rtbbid17us2.%s' % dcash,
                        'rtbbid18us2.%s' % dcash,
                        'rtbbid19us2.%s' % dcash,
                        'rtbbid20us2.%s' % dcash
                        ],
            'rtbesm' :  [
                        'rtbbid11us2.%s' % dcash,
                        'rtbbid12us2.%s' % dcash
                        ],
           }




d_total = 0
u_total = 0

for r in roledefs.iterkeys():
#    print r
    d_role = 0
    u_role = 0
    for h in roledefs[r]:
      status = urllib.urlopen("http://%s/status.txt" %h).read()
      if status.strip() == 'DOWN':
        d_role =  d_role + 1
      elif status.strip() == 'OK':
        u_role = u_role + 1
      else:
#    print "Invalid response, counting as DOWN"
        d_role =  d_role + 1
    ttl = d_role + u_role
    d_pct = (d_role*1.0)/(1.0*d_role+1.0*u_role)*100
    u_pct = (u_role*1.0)/(1.0*d_role+1.0*u_role)*100
    print("%s Cluster -- Members: %s, Down: %s, Up: %s, %%%s Healthy / %%%s Degraded  " %(r, ttl, d_role, u_role, u_pct, d_pct) )

   # d_total = d_total + d_role
   # u_total = u_total + u_role
    
   # if prct >= 25:
   #    print("NOT TAKING DOWN OR ARCHIVE")
   # elif prct < 20:
   #    print("Remove from LB, perform secondary check, and call archive if pass")




