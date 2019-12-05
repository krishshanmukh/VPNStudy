#!/bin/bash

PINGPARSER_PATH=/home/sanjthom/anaconda3/envs/py37/bin/pingparsing

declare -a WEBSITES=("google.com" "google.co.in" "facebook.com" "www.youtube.com" "www.tmall.com" "www.baidu.com" "www.qq.com" "www.sohu.com" "www.taobao.com" "login.tmall.com" "www.wikipedia.org" "360.cn" "Weibo.com" "Sina.com.cn" "www.google.com.ph" "www.google.cn")

i=0
for site in "${WEBSITES[@]}"
do
   echo "Website : $site"
   ping -W 5 -c 10 $site > $site.txt
   PING_TIME_FILES[$i]=$site.txt
   i=$((i+1))
done

$PINGPARSER_PATH ${PING_TIME_FILES[@]} > pingtimes_novpn.json

# start openvpn
LOGIN_FILE=code/login.conf
openvpn --auth-nocache --config ~/Documents/ipvanish-PH-Manila-mnl-a01.ovpn --auth-user-pass $LOGIN_FILE --ca ~/Documents/ca.ipvanish.com.crt &
sleep 10

traceroute google.com > traceroute.txt

PING_TIME_FILES=""
for site in "${WEBSITES[@]}"
do
   echo "Website : $site"
   ping -W 5 -c 10 $site > $site.manila.txt
   PING_TIME_FILES_VPN="$PING_TIME_FILES_VPN $site.manila.txt"
done

$PINGPARSER_PATH $PING_TIME_FILES_VPN > pingtimes_vpn.json

# kill the openvpn process
kill $(ps aux | grep -i 'openvpn --auth-nocache' | head -n 1 | cut -d' ' -f 6)
# waiting for openvpn to shutdown
sleep 4