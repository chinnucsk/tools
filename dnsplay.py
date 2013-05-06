#! /bin/python
import dns.resolver
import dns.query
import dns.zone
import sys
import os


z = dns.zone.from_xfr(dns.query.xfr('10.138.7.101', 'ny.recurly.net'))

names = z.nodes.keys()
names.sort()
for n in names:
  print z[n].to_text()

##import dns.resolver
#import dns.query
#import dns.zone
#from dns.exception import DNSException
#from dns.rdataclass import *
#from dns.rdatatype import *
#
#domain = "dnspython.org"
#print "Getting NS records for", domain
#answers = dns.resolver.query(domain, 'NS')
#ns = []
#for rdata in answers:
#    n = str(rdata)
#    print "Found name server:", n
#    ns.append(n)
#
#for n in ns:
#    print "\nTrying a zone transfer for %s from name server %s" % (domain, n)
#    try:
#        zone = dns.zone.from_xfr(dns.query.xfr(n, domain))
#    except DNSException, e:
#        print e.__class__, e
