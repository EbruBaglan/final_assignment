#! /usr/bin/env python

# import ros stuff
import rospy
from geometry_msgs.msg import Point

from move_base_msgs.msg import MoveBaseActionGoal


# goal
desired_position_ = Point()
desired_position_.x = rospy.get_param('des_pos_x')
desired_position_.y = rospy.get_param('des_pos_y')

move_msg = MoveBaseActionGoal()

move_msg.goal.target_pose.header.frame_id = 'map'
move_msg.goal.target_pose.pose.orientation.w = 1

# callbacks
def clbk_odom(msg):
    global position_
    # position
    position_ = msg.pose.pose.position

def main():
    global pub, active_, desired_position_, move_msg
    i = 0

    rospy.init_node('mod1_user_input')
    
    pub = rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=1)

    desired_position_.x = rospy.get_param('des_pos_x')
    desired_position_.y = rospy.get_param('des_pos_y')

    move_msg.goal.target_pose.pose.position.x = desired_position_.x
    move_msg.goal.target_pose.pose.position.y = desired_position_.y
    move_msg.goal.target_pose.header.frame_id = 'map'
    move_msg.goal.target_pose.pose.orientation.w = 1

    rate = rospy.Rate(20)  
    while not rospy.is_shutdown():
        if i < 100:
            pub.publish(move_msg)
            i= i+1
        else:
            exit()

        rate.sleep()

if __name__ == '__main__':
    main()
