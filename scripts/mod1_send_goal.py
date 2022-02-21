#! /usr/bin/env python

# This node is created to send goals to move_base node.
# Since sending the goal once or all the time did not work,
# this node is created to send the goal and die everytime
# when user wants to reach a new goal. This node is called
# by mod1.py using roslaunch.

# import ros stuff
import rospy
from geometry_msgs.msg import Point
from move_base_msgs.msg import MoveBaseActionGoal

# goal
desired_position_ = Point()
desired_position_.x = rospy.get_param('des_pos_x')
desired_position_.y = rospy.get_param('des_pos_y')

move_msg = MoveBaseActionGoal()

# setting usual parameters
move_msg.goal.target_pose.header.frame_id = 'map'
move_msg.goal.target_pose.pose.orientation.w = 1

# callbacks
def clbk_odom(msg):
    global position_
    position_ = msg.pose.pose.position

def main():
    global pub, active_, desired_position_, move_msg
    i = 0

    rospy.init_node('mod1_send_goal')
    
    # The goal is published on this node.
    pub = rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=1)

    # Parameters are taken.
    desired_position_.x = rospy.get_param('des_pos_x')
    desired_position_.y = rospy.get_param('des_pos_y')

    # Set to message to send.
    move_msg.goal.target_pose.pose.position.x = desired_position_.x
    move_msg.goal.target_pose.pose.position.y = desired_position_.y
    move_msg.goal.target_pose.header.frame_id = 'map'
    move_msg.goal.target_pose.pose.orientation.w = 1

    # Send 100 times, since initial startup takes some time.
    # Can be reduced to decrease waiting time for the upcoming
    # goal inputs.
    rate = rospy.Rate(20)  
    while not rospy.is_shutdown():
        if i < 100:
            pub.publish(move_msg)
            i= i+1
        else:
            exit()
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
