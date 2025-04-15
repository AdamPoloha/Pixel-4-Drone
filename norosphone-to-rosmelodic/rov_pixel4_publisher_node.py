#!/usr/bin/env python
'''
Developer: Adam Poloha + Thein Than Tun
Date: 12 March 2025
Node: BlueROV2 Heavy Configuration, phone sensors Node Publisher
'''

'''
Instructions:
Adam: "catkin_make" to build the package
"roscore"
Adam: include "source ~/catkin_ws/devel/setup.bash" or to run "source ~/catkin_ws/devel/setup.bash && rosrun uuv_sensors rov_phonesocket_publisher_node.py"
"rostopic echo /bluerov2/dp_controller/rov_FNC_phone_data" to check in real-time 
Adam: run "rosrun rviz rviz -f FNC_phone_frame" to start rviz
'''

#Should have 51uT Near New Zealand of geomagnetic field

#/data/data/com.termux/files/usr/libexec/termux-api Sensor -a sensors --es sensors rotation Vector,geomagnetic Rotation Vector
#from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import Imu
import rospy
import numpy as np
import socket
import os
import time

class rov_phone_Pub(object):
	def __init__(self):
		rospy.loginfo("BlueROV2 Heavy Config IMU Node Initialization")

		self._rov_FNC_phone_data_pub = rospy.Publisher('/bluerov2/dp_controller/rov_FNC_phone_data', Imu, queue_size=1)
		self._rov_FNC_phone_data_msg = Imu()
		rospy.loginfo("BlueROV2 Heavy Config phone Node")

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #python2 compatible

		HOST = "192.168.250.154" # Standard loopback interface address (localhost)
		PORT = 1233 # Port to listen on (non-privileged ports are > 1023)

		#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		while True:
			try:
				self.s.bind((HOST, PORT))
				break
			except:
				try:
					#s.shutdown(socket.SHUT_RDWR)
					self.s.close()
					print("Closed")
				except:
					print("Could not close")
					exit()

		self.s.listen(0)
		self.conn, addr = self.s.accept()
		print("Connected by", addr)
		self.buffer = ""


	def read_and_pub(self):
		accels = [0,0,0]
		gyroeul = [0,0,0]
		fusedorient = [0,0,0,0]
		
		while True: #c < 120000: #At -d 5, this loop runs at 200Hz
			data = self.conn.recv(1024) # Grab data from socket
			#print(data)
			if not data:
				print("Received data empty, skipping")
				time.sleep(1)
				return
			self.buffer = self.buffer + data
			parts = self.buffer.split("end")
			#print(len(parts))
			data = parts[0]
			self.buffer = parts[-1] #Section after
			#print(self.buffer)
			
			try:
				#print(data)
				data = data.split("[")
				QO = data[2]
				QO = QO[:-4]
				QO = ' '.join(QO.split())
				fusedorient = list(map(float, QO.split(" ")))
				EW = data[3]
				EW = EW[:-3]
				gyroeul = list(map(float, EW.split(", ")))
				LA = data[4]
				LA = LA[:-1]
				accels = list(map(float, LA.split(", ")))
				break
			except:
				#print("Incomplete data string, skipping")
				a = 0
				return

		self._rov_FNC_phone_data_msg.header.stamp = rospy.Time.now()
		self._rov_FNC_phone_data_msg.header.frame_id = "FNC_phone_frame"
		self._rov_FNC_phone_data_msg.linear_acceleration.x = accels[0]  # linear acceleration x (m/s^2)
		self._rov_FNC_phone_data_msg.linear_acceleration.y = accels[1]  # linear acceleration y (m/s^2)
		self._rov_FNC_phone_data_msg.linear_acceleration.z = accels[2]  # linear acceleration z (m/s^2)
		self._rov_FNC_phone_data_msg.angular_velocity.x = gyroeul[0] # angular velocity x (rad/s)
		self._rov_FNC_phone_data_msg.angular_velocity.y = gyroeul[1] # angular velocity y (rad/s)
		self._rov_FNC_phone_data_msg.angular_velocity.z = gyroeul[2] # angular velocity z (rad/s)
		self._rov_FNC_phone_data_msg.orientation.x = fusedorient[0]
		self._rov_FNC_phone_data_msg.orientation.y = fusedorient[1]
		self._rov_FNC_phone_data_msg.orientation.z = fusedorient[2]
		self._rov_FNC_phone_data_msg.orientation.w = fusedorient[3]

		#print("Publishing")
		self._rov_FNC_phone_data_pub.publish(self._rov_FNC_phone_data_msg)

		#self.closeport()

	def closeport(self):
		try:
			#s.shutdown(socket.SHUT_RDWR)
			self.s.close()
			print("Closed")
		except:
			print("Could not close")

	def shutdownhook(self):
		rospy.loginfo("Shut Down.")
		rospy.loginfo("Closing phone sensors socket")
		self.closeport()
		rospy.loginfo("Done")
		ctrl_c = True
		#exit()

if __name__ == '__main__':
	rospy.init_node('rov_phone_Pub_node')
	rov_phone_Pub_object = rov_phone_Pub()
	rate = rospy.Rate(102) # loop Hz
	ctrl_c = False

	rospy.on_shutdown(rov_phone_Pub_object.shutdownhook)
	while not ctrl_c:
		try:
			rov_phone_Pub_object.read_and_pub()
			rate.sleep()
		except KeyboardInterrupt:
			rospy.loginfo("Closing IMU Port")
			rov_phone_Pub_object.closeport()
			rospy.loginfo("Done")
			ctrl_c = True
			#exit()
		except IOError:
			rospy.loginfo("Port is closed")
			exit()
		except Exception as e:
			rospy.loginfo(e)
			exit()
