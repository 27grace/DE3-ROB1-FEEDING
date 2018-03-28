# !/usr/bin/env python

from math import sqrt
from baxter_control import BaxterControl
import baxter_interface
import roslib
import sys
import rospy
from message_filters import Subscriber
from geometry_msgs.msg import Point


SPEED_CONST = 100
MIN_SPEED = 0.01


def get_difference_between_points(a, b):
    return b.x - a.x, b.y - a.y, b.z - a.z


def get_distance_between_points(a, b):
    dx, dy, dz = get_difference_between_points(a, b)
    return sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))


def get_direction_between_points(a, b):
    dx, dy, dz = get_difference_between_points(a, b)
    mag = get_distance_between_points(a, b)
    return [dx / mag, dy / mag, dz / mag]


# Move endpoint to where we want it by solving IK and using joint velocities. Hopefully this works
class KinematicControl:
    def __init__(self):
        self.ik_solution = None
        self.required_joint_velocities = None

    def set_desired_endpoint(self, desired_endpoint):
        # TODO: Use baxter IK Service to set self.ik_solution to required joint movements for desired_endpoint
        self.ik_solution = None # = solution. should be dict {joint_name : required_angle_change}
        pass

    def set_joint_velocities(self, speed):
        self.required_joint_velocities = {}
        max_joint_change = max([abs(angle) for angle in self.ik_solution.values()])
        for joint, required_angle_change in self.ik_solution:
            max_joint_change_ratio = required_angle_change / max_joint_change
            self.required_joint_velocities[joint] = max_joint_change_ratio

    # speed should be between 0.0 and 0.5 (i.e. is ratio of max speed)
    def move_to_desired_endpoint(self, desired_endpoint, speed):
        limb = baxter_interface.Limb('right')
        limb.set_joint_velocities(self.required_joint_velocities)


class ReactiveControl:
    def __init__(self, baxter_control):
        self.baxter_control = baxter_control
        self.mouth_subscription = None
        self.food_subscription = None
        self.food_point = None
        self.mouth_point = None
        self.distance = None
        self.direction = None
        self.speed = None
        self.kinematic_control = KinematicControl()

    def turn_on(self):
        if self.mouth_subscription is None and self.food_subscription is None:
            self.mouth_subscription = rospy.Subscriber("/mouth_xyz_astra", Point, self.__mouth_callback__)
            self.food_subscription = rospy.Subscriber("/mouth_xyz_astra", Point, self.__food_callback__)

    def turn_off(self):
        if self.mouth_subscription is not None and self.food_subscription is not None:
            self.mouth_subscription.unregister()
            self.food_subscription.unregister()
            self.food_subscription = None
            self.mouth_subscription = None

    # TODO: Testing for right speed ratios
    def set_speed(self):
        if self.__points_valid__():
            self.speed = MIN_SPEED + self.distance / SPEED_CONST

    def __points_valid__(self):
        return self.food_point is not None and self.mouth_point is not None

    # Callback for mouthxyz changes. Make sure we subscribe with this as callback!
    def __mouth_callback__(self, mouth_point):
        self.mouth_point = mouth_point
        self.__update_values__()

    # Callback for foodxyz changes. Make sure we subscribe with this as callback!
    def __food_callback__(self, food_point):
        self.food_point = food_point
        self.__update_values__()

    def __set_distance__(self):
        if self.__points_valid__():
            self.distance = get_distance_between_points(self.food_point, self.mouth_point)

    def __set_direction__(self):
        if self.__points_valid__():
            self.direction = get_direction_between_points(self.food_point, self.mouth_point)

    def __update_values__(self):
        self.__set_distance__()
        self.__set_direction__()
        self.set_speed()
        self.__update_robot_motion__()

    def __update_robot_motion__(self):
        self.baxter_control.set_ee_pos(self.mouth_point.x, self.mouth_point.y, self.mouth_point.z)


def main(args):
    baxter_control = BaxterControl()
    rc = ReactiveControl(baxter_control)
    rospy.init_node('Reactive', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    print("Reactive Control")
    main(sys.argv)
