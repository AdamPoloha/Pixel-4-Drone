#!/bin/bash

#Looks for adb device, then finds IP address

while true;
do
	devs="$(adb devices)"
	#echo $devs
	tmp=${devs#*Z006K5}   # remove prefix ending in "CSTDU"
	#echo $tmp
	echo "Waiting for phone ADB"
	if [ "$tmp" == "$devs" ]
	then
		echo "Connect phone, or reconnect"
		sleep 0.5s
	else
		break
	fi
done

echo "ADB device connected"
#echo "Wait 15 seconds"
#sleep 15s

while true;
do
	ips="$(adb shell ifconfig)"
	#echo $ips
	tmp=${ips#*rndis0}   # remove prefix ending in "192.168.42."
	#echo $tmp
	echo "Checking IP addresses"
	if [ "$tmp" == "$ips" ]
	then
		echo "Phone IP not found"
		sleep 0.5s
	else
		break
	fi
done

tmp=${tmp#*192.168.}
tmp=${tmp//Bcast*}
tmp="$(echo $tmp | xargs)"
#echo $tmp

net=$(echo $ip | cut -f3 -d.)
#net=192.169.$net
#echo $net

while true;
do
	ips="$(hostname -I)"
	#echo $ips
	tmp2=${ips#*192.168.$net}
	#echo $tmp2
	echo "Checking IP addresses"
	if [ "$tmp" == "$ips" ]
	then
		echo "Phone network not found"
		sleep 0.5s
	else
		break
	fi
done

ip=192.168.$tmp
echo "Phone IP on tether network is: "$ip
ippc=192.168.$net$tmp2
echo "My IP on phone network is: "$ippc

echo "SSH by: ssh u0_a235@"$ip" -p 8022"

#echo "Wait 10 seconds"
#sleep 10s
#echo "Running code through ssh"
echo "sshpass -p sub ssh u0_a235@"$ip" -p 8022 ~/localisation/OrientSend.sh "$ippc
