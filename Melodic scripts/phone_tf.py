#!/usr/bin/env python
'''
Developer: Adam Poloha
Date: 20 November 2024
rosrun pixel4sub phone_tf.py
'''
import rospy
 
import tf
 
#from uuv_control_msgs.msg import Performance_index, Orientation_rpy, Updated_alpha
#from geometry_msgs.msg import Quaternion
from tf.transformations import euler_from_quaternion, quaternion_from_euler
#from geometry_msgs.msg import TwistStamped,WrenchStamped, PoseArray, Pose
 
from sensor_msgs.msg import Imu
 
class phone_TF(object):
 
	_LABEL = 'Phone frame visual'
	 
	def __init__(self):
		self._tf_broadcaster = tf.TransformBroadcaster()
		self._imu_phone = rospy.Subscriber('Drone_FNC_phone_data', Imu, self.imu_callback,queue_size=10)
		print("Initialised")
		self.T = 0.0026 # 0.0098 # 1 / 102Hz
		self.reset_tf()

	def reset_tf(self):
		self.xv = 0
		self.yv = 0
		self.zv = 0
		self.xd = 0
		self.yd = 0
		self.zd = 0

	def reset_d(self):
		self.xd = 0
		self.yd = 0
		self.zd = 0

	def integrate(self, scalar, T):
		return scalar * T

	def imu_callback(self,msg):
		#print("Extracting message values")
		x = msg.orientation.x
		y = msg.orientation.y
		z = msg.orientation.z
		w = msg.orientation.w
		#print("Normalising")
		eul = euler_from_quaternion([x,y,z,w])
		q = quaternion_from_euler(eul[0],eul[1],eul[2])
		#q = Quaternion(x,y,z,w)
		#q = tf.transformations.quaternion_normalize([x,y,z,w])
		#q = tf.transformations.unit_vector([x,y,z,w])
		
		#print(q)
		x = q[0]
		y = q[1]
		z = q[2]
		w = q[3]

		xa = msg.linear_acceleration.x
		ya = msg.linear_acceleration.y
		za = msg.linear_acceleration.z

		self.xv = self.xv + self.integrate(xa, self.T)
		self.yv = self.yv + self.integrate(ya, self.T)
		self.zv = self.zv + self.integrate(za, self.T)

		self.xd = self.xd + self.integrate(self.xv, self.T)
		self.yd = self.yd + self.integrate(self.yv, self.T)
		self.zd = self.zd + self.integrate(self.zv, self.T)

		print(self.xv,self.yv,self.zv)

		self._tf_broadcaster.sendTransform((self.xd,self.yd,self.zd), #self._mhe_states[0],self._mhe_states[1],self._mhe_states[2]),
		   (x,y,z,w),
		   rospy.Time.now(),
		   "FNC_phone_frame",
		   "world")
	 
	 
	def shutdownhook(self):
		rospy.loginfo("Shut Down.")
		 
		ctrl_c = True
 
if __name__ == '__main__':
	rospy.init_node('phone_TF')
	phone_TF_object = phone_TF()
	rate = rospy.Rate(1)
	ctrl_c = False
 
	rospy.on_shutdown(phone_TF_object.shutdownhook)
	while not ctrl_c:
		try:
			phone_TF_object.reset_d()
			rate.sleep()
		except KeyboardInterrupt:
			ctrl_c = True
			exit()
		except IOError:
			exit()
		except Exception as e:
			rospy.loginfo(e)
			exit()
