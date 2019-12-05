#!/bin/bash

PYTHON_EXEC=/home/sanjthom/anaconda3/bin/python

# start openvpn
LOGIN_FILE="login.conf"
CACERT_FILE="/home/sanjthom/Documents/ca.ipvanish.com.crt"
CONFIG_DIR="/home/sanjthom/Documents/"
# ipvanish-PH-Manila-mnl-a01.ovpn
declare -a VPN_SERVERS=("ipvanish-US-New-York-nyc-a01.ovpn" "ipvanish-US-Seattle-sea-a01.ovpn" "ipvanish-ZA-Johannesburg-jnb-c01.ovpn" "ipvanish-US-Atlanta-atl-a01.ovpn" "ipvanish-UK-London-lon-a01.ovpn" "ipvanish-UA-Kiev-iev-c01.ovpn" "ipvanish-SI-Ljubljana-lju-c02.ovpn" "ipvanish-SK-Bratislava-bts-c01.ovpn")
declare -a SHORT_NAMES=("nyc" "sea" "jnb" "atl" "lon" "iev" "lju" "bts")

i=0
for vpn_server in "${VPN_SERVERS[@]}"
do
	VPN_SERVER_LOC="$CONFIG_DIR$vpn_server"
	openvpn --auth-nocache --config $VPN_SERVER_LOC --auth-user-pass $LOGIN_FILE --ca $CACERT_FILE &
	sleep 6

	echo "----------------------------------------------------------------------------"
	touch plt_${SHORT_NAMES[$i]}.json
	$PYTHON_EXEC prt.py ${SHORT_NAMES[$i]}
	echo "----------------------------------------------------------------------------"
	i=$((i+1))

	# kill the openvpn process
	kill $(ps aux | grep -i 'openvpn --auth-nocache' | head -n 1 | awk '{print $2}')
	# waiting for openvpn to shutdown
	sleep 4

done