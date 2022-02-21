#!/usr/bin/env python

# This node is used to manipulate teleopt_twist_keyboard outputs,
# so that the suicidal user will not hit the wall. Mainly, if there
# is an obstacle, and the user wants to ride in that direction,
# the velocity in that direction is zeroed. Code is mostly taken
# from the lecture slides, considering only front, fright and fleft directions.

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

vel_ = Twist()
vel_.linear.x = 0.0
vel_.angular.z = 0.0 

# Final output is published on real /cmd_vel
pub = rospy.Publisher("/cmd_vel", Twist)

# This part is from lecture slides. Zeroing obstacle direction velocity.
def take_action(regions):
    msg = Twist()
    linear_x = vel_.linear.x
    angular_z = vel_.angular.z

    state_description = ''

    if regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 2 - front'
        if linear_x > 0:
            linear_x = 0
    elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 3 - fright'
        if angular_z < 0:
            angular_z = 0
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 4 - fleft'
        if angular_z > 0:
            angular_z = 0
    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 5 - front and fright'
        if linear_x > 0 or angular_z < 0:
            linear_x = 0
            angular_z = 0
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 6 - front and fleft'
        if linear_x > 0 or angular_z > 0:
            linear_x = 0
            angular_z = 0
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 7 - front and fleft and fright'
        if linear_x > 0:
            linear_x = 0
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 8 - fleft and fright'
        if angular_z != 0:
            angular_z = 0
    else:
        state_description = 'unknown case'
        #rospy.loginfo(regions)

    #rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

# From lecture slides. Only front, fright, fleft directions are considered.
def clbck_laser(msg):
    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }
    take_action(regions)
    
def clbck2(msg):
    global vel_
    vel_ = msg

def controller():
    rospy.init_node("mod3_controller")

    # /scan and /cmd_vel_raw messages are taken to manipulate user input.
    rospy.Subscriber('/scan', LaserScan, clbck_laser)
    rospy.Subscriber('/cmd_vel_raw', Twist, clbck2)   
    rospy.spin()

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass