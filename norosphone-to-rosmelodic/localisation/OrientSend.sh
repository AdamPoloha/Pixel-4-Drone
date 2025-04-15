#!/data/data/com.termux/files/usr/bin/sh

echo "Sending to ip: "$1

while true;
do
        python ~/localisation/rov_phone_sender.py $1
        sleep 3s
        echo "Retry"
done