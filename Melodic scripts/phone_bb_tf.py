#!/usr/bin/env python
'''
Developer: Adam Poloha
Date: 20 November 2024
rosrun pixel4sub phone_bb_tf.py
'''
import rospy
 
import tf
import math
 
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

	def imu_callback(self,msg):
		#print("Extracting message values")
		x = msg.orientation.x
		y = msg.orientation.y
		z = msg.orientation.z
		w = msg.orientation.w
		#print("Normalising")

		"""
		n = math.sqrt(x**2 + y**2 + z**2 + w**2)
		x = x/n
		y = y/n
		z = z/n
		w = w/n
		"""
		eul = euler_from_quaternion([x,y,z,w])
		
		sp = eul[0]
		sr = eul[1]
		sy = eul[2]
		
		#print(sp,sr,sy)

		bbp = -sy
		bbr = sr + (math.pi/2)
		bby = sp

		#print(bbp,bbr,bby)

		q = quaternion_from_euler(bbp,bbr,bby)
		#q = quaternion_from_euler(eul[0],eul[1],eul[2])
		#q = Quaternion(x,y,z,w)
		#q = tf.transformations.quaternion_normalize([x,y,z,w])
		#q = tf.transformations.unit_vector([x,y,z,w])
		
		#print(q)
		x = q[0]
		y = q[1]
		z = q[2]
		w = q[3]

		self._tf_broadcaster.sendTransform((0,0,0), #self._mhe_states[0],self._mhe_states[1],self._mhe_states[2]),
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
			rate.sleep()
		except KeyboardInterrupt:
			ctrl_c = True
			exit()
		except IOError:
			exit()
		except Exception as e:
			rospy.loginfo(e)
			exit()
