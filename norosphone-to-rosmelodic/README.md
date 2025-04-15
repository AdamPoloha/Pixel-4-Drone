This set of scripts was used to get sensor data from the Pixel 4 to a BlueROV2 UUV. The phone was inside the housing and the data was received by the controlling Raspberry Pi 4.

The localisation folder goes into the termux home folder on the phone (sensor.sh is expected to be running on bootup), and the other two scripts go into the ROS package scripts folder made for ROS Melodic.

Running OrientLaunch4.sh should output the command that is needed to launch everything on the phone side. Then rov_pixel4_publisher_node.py needs to be edited to set the correct IP address of the PC/Raspberry Pi.

Running the node with ROS should then publish the phone orientation.

If it does not work, I likely have not uploaded the latest bug-fixed version of the scripts trapped inside the BlueROV2. Please let me know.
