# Pixel-4-Drone
A repository with all things relating to sensors, localisation, and control of drones with a Pixel 4 Phone.

# Autoboot on power like Raspberry Pi
In adb:
  adb reboot bootloader
In fastboot:
  fastboot oem off-mode-charge 0

# Network
Can set USB tethering as the default USB configuration and it works, make sure to disable device/screen lock so that it does not have to wait for unlock to enable.
MAC address changes on every boot for phone, and then IP for both devices.

# Termux and SSH
Follow: [Multicopter-phone-ROS](https://raw.githubusercontent.com/AdamPoloha/Multicopter-phone-ROS/refs/heads/main/README.md)
Username: u0_a235
Password: sub
ssh u0_a235@192.168.103.238 -p 8022

# Ubuntu, ROS, CASADI
Follow: [Android-ROS-Melodic-and-Casadi](https://raw.githubusercontent.com/AdamPoloha/Android-ROS-Melodic-and-Casadi/refs/heads/main/README.md)
Older Ubuntu: apt-get autoremove --purge snapd

# XVNC
Inside Ubuntu terminal session:
  apt install xvfb x11vnc
  wget https://raw.githubusercontent.com/AdamPoloha/Multicopter-phone-ROS/refs/heads/main/startxvnc.sh
  chmod +x ./startxvnc.sh
  exit
Then in Termux:
  
