# Pixel-4-Drone
A repository with all things relating to sensors, localisation, and control of drones with a Pixel 4 Phone.

# Autoboot on power like Raspberry Pi
In adb:
  adb reboot bootloader
In fastboot:
  fastboot oem off-mode-charge 0

# Network
Can set USB tethering as the default USB configuration and it works, make sure to disable device/screen lock so that it does not have to wait for unlock to enable.
Remember to turn on "Disable adb authorisation timout" in Developer options if you want to use adb without touching the phone, making sure adb does not revoke your debugger device after 7 days.
MAC address changes on every boot for phone, and then IP for both devices.
Pixel4IPFinder.sh will be able to check adb for the phone's IP and find the PC's IP based on that, then it will give the command for SSH.

# Termux and SSH
Follow: [Multicopter-phone-ROS](https://github.com/AdamPoloha/Multicopter-phone-ROS/blob/main/README.md?plain=1)
Username: u0_a235
Password: sub
ssh u0_a235@192.168.103.238 -p 8022

# Ubuntu, ROS, CasADi
Follow: [Android-ROS-Melodic-and-Casadi](https://github.com/AdamPoloha/Android-ROS-Melodic-and-Casadi/blob/main/README.md?plain=1) and [Termux Desktops](https://github.com/LinuxDroidMaster/Termux-Desktops/blob/main/Documentation/chroot/ubuntu_chroot.md)
sudo curl https://cdimage.ubuntu.com/ubuntu-base/releases/22.04.5/release/ubuntu-base-22.04.5-base-amd64.tar.gz --output ubuntu.tar.gz

# XVNC
Inside Ubuntu terminal session:
  apt install xvfb x11vnc
  wget https://raw.githubusercontent.com/AdamPoloha/Multicopter-phone-ROS/refs/heads/main/startxvnc.sh
  chmod +x ./startxvnc.sh
  exit
On every start:
  ./startxvnc.sh

# Sensors
Follow: [Multicopter-phone-ROS](https://github.com/AdamPoloha/Multicopter-phone-ROS/blob/main/README.md?plain=1)
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

"Gravity Sensor" is stable enough that is may be completely usable, "Linear Acceleration Sensor" is chaotic despite this.
"Orientation Sensor" has weird behaviour where pitch can have a max of 180 degrees, and roll 90. Roll 90 turns into 180 on the pitch. Read about it straight from the perpetrators: https://source.android.com/docs/core/interaction/sensors/sensor-types#orientation_deprecated

I will use "Game Rotation Vector Sensor","Geomagnetic Rotation Vector Sensor","LSM6DSR Gyroscope","LSM6DSR Accelerometer","LIS2MDL Magnetometer" and "Gravity Sensor".
Mine: termux-sensor -s "Game Rotation Vector Sensor","Geomagnetic Rotation Vector Sensor","LSM6DSR Gyroscope","LSM6DSR Accelerometer","LIS2MDL Magnetometer","Gravity Sensor" -d 1 | nc 127.0.0.1 1234
Message Order: Acc, Mag, Gyro, Game, Geo, Grav

# Drone Package
Make Package (https://docs.ros.org/en/eloquent/Tutorials/Creating-Your-First-ROS2-Package.html)
Ubuntu Terminal:
  mkdir ~/ros2_ws
  mkdir ~/ros2_ws/src
  cd ~/ros2_ws/src
  ros2 pkg create --build-type ament_python --node-name hello_node phone_drone
  cd ~/ros2_ws
  colcon build
  . install/setup.bash
  ros2 run phone_drone hello_node
Ubuntu Terminal:
  cd ~/ros2_ws/src/phone_drone/phone_drone
  wget https://raw.githubusercontent.com/AdamPoloha/Multicopter-phone-ROS/refs/heads/main/phone_sensor_publisher_node.py
  apt install geany
  geany ../setup.py
  Add new entry point to console_scripts
'phone_sensor_publisher_node = phone_drone.phone_sensor_publisher_node.py'

# GPS
If you use termux-location and you get the following error:
  "error": "Please grant the following permission to use this command: android.permission.ACCESS_FINE_LOCATION"
Open app management, Termux:API, and then enable all permissions or just location.
