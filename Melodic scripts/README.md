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

# Sub Package ROS Melodic
Follow: [Creating a ROS Package](https://wiki.ros.org/ROS/Tutorials/CreatingPackage)
  mkdir ~/ros_ws
  mkdir ~/ros_ws/src
  cd ~/ros_ws/src
  catkin_create_pkg pixel4sub std_msgs rospy
  cd ~/ros_ws
  catkin_make
  echo "source /root/ros_ws/devel/setup.bash" >> ~/.bashrc
  source ~/.bashrc
  mkdir ~/ros_ws/src/pixel4sub/scripts
  cd ~/ros_ws/src/pixel4sub/scripts
  wget https://raw.githubusercontent.com/AdamPoloha/Pixel-4-Drone/refs/heads/main/Melodic%20scripts/phone_sensor_publisher_node.py
  wget https://raw.githubusercontent.com/AdamPoloha/Pixel-4-Drone/refs/heads/main/Melodic%20scripts/phone_bb_tf.py
  wget https://raw.githubusercontent.com/AdamPoloha/Pixel-4-Drone/refs/heads/main/Melodic%20scripts/phone_tf.py
  chmod +x phone_sensor_publisher_node.py
  cd ~/ros_ws
  catkin_make
  python2 -m pip install pysocket
One Terminal:
  roscore
Second:
  rosrun pixel4sub phone_sensor_publisher_node
Third:
  rosrun pixel4sub phone[_bb]_tf.py
Fourth:
  rosrun rviz rviz -f world
Then in rviz add tf and IMU.
