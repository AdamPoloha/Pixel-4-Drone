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
	tmp=${ips#*addr:10.}
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

tmp=10.$tmp
tmp=${tmp//Bcast*}
tmp="$(echo $tmp | xargs)"

net=$(echo $tmp | cut -f2 -d.).$(echo $tmp | cut -f3 -d.)

while true;
do
	ips="$(hostname -I)"
	#echo $ips
	tmp2=${ips#* 10.$net}
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

echo "Phone IP on tether network is: "$tmp
ippc=10.$net$tmp2
echo "My IP on phone network is: "$ippc

echo "SSH by: ssh u0_a235@"$tmp" -p 8022"
