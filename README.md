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
Pixel4IPFinder.sh will be able to check adb for the phone's IP and find the PC's IP based on that, then it will give the command for SSH.

# Termux and SSH
Follow: [Multicopter-phone-ROS](https://raw.githubusercontent.com/AdamPoloha/Multicopter-phone-ROS/refs/heads/main/README.md)
Username: u0_a235
Password: sub
ssh u0_a235@192.168.103.238 -p 8022

# Ubuntu, ROS, CasADi
Follow: [Android-ROS-Melodic-and-Casadi](https://raw.githubusercontent.com/AdamPoloha/Android-ROS-Melodic-and-Casadi/refs/heads/main/README.md)
Older Ubuntu: apt-get autoremove --purge snapd

# CasADi Speed Test
mkdir ./casaditest
cd ./casaditest
wget https://raw.githubusercontent.com/AdamPoloha/Pixel-4-Drone/refs/heads/main/CasADi/mpc_code.py
python2 ./mpc_code.py
Results:
  ('Total time: ', 9.567008972167969) normal
  ('Total time: ', 6.1133880615234375) performance governor
  ('Total time: ', 5.061182022094727) all-core max frequency
  ('Total time: ', 4.859670877456665)
  Average no IPOPT verbose: 5s
Average Result for i7 9700: 4.93s

# XVNC
Inside Ubuntu terminal session:
  apt install xvfb x11vnc
  wget https://raw.githubusercontent.com/AdamPoloha/Multicopter-phone-ROS/refs/heads/main/startxvnc.sh
  chmod +x ./startxvnc.sh
  exit
On every start:
  ./startxvnc.sh

# Sensors
Follow: [Multicopter-phone-ROS](https://raw.githubusercontent.com/AdamPoloha/Multicopter-phone-ROS/refs/heads/main/README.md)
  "LSM6DSR Accelerometer", [X,Y,Z] (m/s^2)
  "LIS2MDL Magnetometer", [X,Y,Z] (untested units)
  "LSM6DSR Gyroscope", [X,Y,Z] (Probably radians/s)
  "TMD3702V Ambient Light Sensor",
  "BMP380 Pressure Sensor", [1 Value] (millibars)
  "TMD3702V Proximity Sensor (wake-up)",
  "LIS2MDL Magnetometer-Uncalibrated", [6 Values, 3 Active, X,Y,Z]
  "LSM6DSR Gyroscope-Uncalibrated", [6 Values, X,Y,Z, and 3 random]
  "LSM6DSR Accelerometer-Uncalibrated", [6 Values, X,Y,Z, and 3 constants]
  "MAX11261 Edge-Detect Sensor",
  "LSM6DSR Temperature",
  "BMP380 Temperature",
  "LIS2MDL Temperature",
  "camera v-sync 0",
  "camera v-sync 1",
  "camera v-sync 2",
  "TMD3702V Color Sensor",
  "VD6282 Rear Light",
  "Combo Light",
  "Binned Brightness",
  "Device Pickup Sensor",
  "Proximity Gated Single Tap Gesture",
  "Double Twist", [empty]
  "Front Camera Light",
  "Game Rotation Vector Sensor", [X,Y,Z,W] (Should be Gyro Integrated Quaternion)
  "Geomagnetic Rotation Vector Sensor", [5 Values, X,Y,Z,W,unknown] (Magnetometer/Compass Quaternion)
  "Gravity Sensor", [X,Y,Z] (Gravity extracted from Accelerometer)
  "Linear Acceleration Sensor", [X,Y,Z] (Gravity removed from Accelerometer)
  "Orientation Sensor", [Y,P,R] (Degrees, should have some sensor fusion)
  "Rotation Vector Sensor", -> "Game Rotation Vector Sensor"
  "Significant Motion",
  "Step Counter",
  "Step Detector",
  "Tilt Sensor", [1 value]
  "Device Orientation", [1 value]
  "Device Orientation Debug", [empty]
  "Rotation preindication", [Empty -> 16 Values, 1 Active] (No clue what they mean)

Gravity Sensor is stable enough that is may be completely usable, Linear Acceleration Sensor is chaotic despite this.
