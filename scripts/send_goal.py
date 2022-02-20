#! /usr/bin/env python

# This state machine code is adapted from go_to_point_service_m.py of last topics
# Source: https://github.com/CarmineD8/robot_description/tree/noetic-laser

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf import transformations

from move_base_msgs.msg import MoveBaseActionGoal
from actionlib_msgs.msg import GoalID


# added from presentations, to publish on move_base
move_msg = MoveBaseActionGoal()
move_msg.goal.target_pose.header.frame_id = 'map'
move_msg.goal.target_pose.pose.orientation.w = 1

# goal
desired_position_ = Point()
desired_position_.x = rospy.get_param('des_pos_x')
desired_position_.y = rospy.get_param('des_pos_y')

def clbk_odom(msg):
    global position_
    global yaw_

    # position
    position_ = msg.pose.pose.position

def sendGoal(des_pos):
    move_msg.goal.target_pose.pose.position.x = des_pos.x
    move_msg.goal.target_pose.pose.position.y = des_pos.y
    pub.publish(move_msg)

def main():
    global pub, active_, desired_position_

    rospy.init_node('send_goal')

    # changed from /cmd_vel to this
    pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=1)

    # https://answers.ros.org/question/57772/how-can-i-cancel-a-navigation-command/
    pub1 = rospy.Publisher('/move_base/cancel', GoalID, queue_size=1)

    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        desired_position_.x = rospy.get_param('des_pos_x')
        desired_position_.y = rospy.get_param('des_pos_y')
        if not active_:
            continue
        else:
            sendGoal(desired_position_)

        rate.sleep()


if __name__ == '__main__':
    main()
