#!/usr/bin/env python
# coding: utf-8

# TODO
# get the various paths that are taken from our machine to the destination for various VPN services.
# calculate the time in multiple cases and record the average time
# take a screenshot of dns leak on ubuntu
# ping
# ping vpn server with and without vpn
# ping with/without vpn, location specific content with vpn
# page response time
# traceroute

import json
import matplotlib.pyplot as plt
import numpy as np
from scapy.all import *


IPVANISH_HOMEDIR = "/home/sanjthom/Documents"
ovpn_files = ['ipvanish-AL-Tirana-tia-c02.ovpn','ipvanish-US-New-York-nyc-a01.ovpn']

target = 'google.com'

# DNS Resolution
answer = sr1(IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=target)),verbose=0)
target_ip = answer.an.rdata
print("DNS resolved: {} ==> {}".format(target,target_ip))
print()


def get_pingtimes(target_ip,count):
    resp_times = []
    for i in range(count):
        response = sr(IP(dst=target_ip) / ICMP(id=100),timeout=5,verbose=0)
        # first entry of response is the answered list of packet pairs
        # first entry of next list gives us ICMP packet pairs
        # the packet pair consists of packet sent and received
        if len(response) != 0:
            resp_times.append(response[0][0][1].time - response[0][0][0].time)
    return resp_times


#ping_times = get_pingtimes(target_ip,10)
#mean_pingtime = np.mean(ping_times)


# shanmukh's ip geolocation lookup
# a db of ip to  geolocation,AS mappings:
# https://dev.maxmind.com/geoip/geoip2/geolite2/
import json
import geoip2.database
from ip2geotools.databases.noncommercial import DbIpCity

#try:
#    db = geoip2.database.Reader("GeoLite2-ASN.mmdb")
#except Exception:
#    warning("Cannot open geoip2 database")

def get_location(target):
    try:
        result = json.loads(DbIpCity.get(target, api_key='free').to_json())
    except:
        result = {'city': 'Stony Brook', 'country': 'US'}
    
    #try:
    #    asn = db.asn(target).autonomous_system_organization
    #except geoip2.errors.AddressNotFoundError:
    #    asn = "N.A."
    #print(result)

    return result['city'],result['country']


# TCP Traceroute
from scapy.layers.inet import traceroute
from scapy.layers.inet import traceroute_map

# ans,unans = answered,unanswered packets list
# They are of type TracerouteResult defined in scapy/inet.py
# each entry in ans is a 2-entry tuple = send,recv packet
ans,unans = traceroute(target, maxttl=60, verbose=0)
index = len(ans)
for i,v in enumerate(ans):
    if v[0].dst == v[1].src:
        index = i
        break

# scapy parallelly sends requests for all TTL's and stores results from them.
# Removing redundant entries after the packet reaches destination
ans = ans[0:index+1]


print("List of answered packets:")
print()

print("Target: {}:".format(ans[0][0].dst))
for s,d in ans:
    src = s.sprintf("Hop: %03s,IP.ttl%")
    city,country = get_location(d.src)
    dst = d.sprintf(", Address: %15s,IP.src%, Location: "+city+","+country)
    print(src+dst)


print("Thee are {} unanswered packets.".format(len(unans)))

if len(unans) != 0:
    print("List of unanswered packets:")
    print()
    print("TTL  Source IP      Port")
    for s in unans:
        print(s.sprintf("%-03s,IP.ttl%  %IP.dst%  {TCP:%ir,TCP.dport%}{UDP:udp%ir,UDP.dport%}"))


#from scapy.config import conf

#conf.geoip_city = "/home/sanjthom/FCN/geolite2/GeoLite2-City.mmdb"
#lines = traceroute_map(target_ip)
