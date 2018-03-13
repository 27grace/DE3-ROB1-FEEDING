# !/usr/bin/env python


from math import sqrt
from baxter_control import BaxterControl
import baxter_interface
import roslib
import sys
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Point
import argparse
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from std_msgs.msg import Header
from baxter_core_msgs.srv import SolvePositionIK, SolvePositionIKRequest


class ReactiveControl:
	def __init__(self):
		#self.food_point = None
		self.mouth_point = rospy.Subscriber("/mouth_xyz_astra", Point, self.mouth_callback)
		print self.mouth_point
		print "Subscribed"
		#self.distance = None
		#self.direction = None
		#self.speed = None
		#self.kinematic_control = KinematicControl()

	# def points_valid(self):
	# 	return self.food_point is not None and self.mouth_point is not None

	# Callback for mouthxyz changes. Make sure we subscribe with this as callback!
	def mouth_callback(self,  mouth_point):
		print "mouth callback"
		self.mouth_point = mouth_point
		self.update_values()

	# # Callback for foodxyz changes. Make sure we subscribe with this as callback!
	# def food_callback(self, food_point):
	# 	self.food_point = food_point
	# 	self.update_values()

	# def set_distance(self):
	# 	if self.points_valid():
	# 		self.distance = get_distance_between_points(self.food_point, self.mouth_point)

	# def set_direction(self):
	# 	if self.points_valid():
	# 		self.direction = get_direction_between_points(self.food_point, self.mouth_point)

	# TODO: Testing for right speed ratios
	# def set_speed(self):
	# 	if self.points_valid():
	# 		self.speed = MIN_SPEED + self.distance / SPEED_CONST

	def update_values(self):
		#self.set_distance()
		#self.set_direction()
		#self.set_speed()
		self.update_robot_motion()

	def update_robot_motion(self):
		fred.set_end_effector_pos(self.mouth_point.x, self.mouth_point.y, self.mouth_point.z)


def main(args):
	
	rospy.init_node('Reactive', anonymous=True)
	
	
	#food_point = ReactiveControl.food_callback(fred.get_ee_pos('right'))
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")

def print_data(data):
	print "hello"

if __name__ == '__main__':
	print("Test Motion")
	fred = BaxterControl()
	controlling = ReactiveControl()
	main(sys.argv)


