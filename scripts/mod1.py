#! /usr/bin/env python

# This node is created to initiate mod1_send_goal node
# everytime user sends a new input. Roslaunch is used for
# this purpose. When the goal is within a threashold distance,
# the goal is considered to be reached and asked user for
# new goal position.

import rospy
import roslaunch
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
import os
from actionlib_msgs.msg import GoalStatusArray
from datetime import datetime

position_ = Point()

# callbacks
def clbck(msg):
	global position_
	position_ = msg.pose.pose.position

# the function to initiate mod1_send_goal
def start_task():
    rospy.loginfo("starting...")

    package = 'final_assignment'
    executable = 'mod1_send_goal.py'
    node = roslaunch.core.Node(package, executable)

    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()

    script = launch.launch(node)
    print(script.is_alive())

def main():
    threshold = 0.6
    rospy.init_node('mod1')

    # The first goal positions are taken from parameter server
    x = rospy.get_param("des_pos_x")
    y = rospy.get_param("des_pos_y")
    os.system('clear')
    print("Hi! We are reaching the first position: x = " + str(x) + ", y = " + str(y))
    start_task()
    # clear is widely used to avoid log outputs of roslaunch
    os.system('clear')
    print("Hi! We are reaching the first position: x = " + str(x) + ", y = " + str(y))
    
    sub = rospy.Subscriber('/odom', Odometry, clbck)
    start_time = datetime.now()
    timeout_ = False

    rate = rospy.Rate(20)
    
    while not rospy.is_shutdown():    
        time_delta = datetime.now() - start_time
        if time_delta.total_seconds() > 90:
            timeout_=True
        
        if abs(x-position_.x) <= threshold and abs(y-position_.y) <= threshold and not timeout_:
            os.system('clear')
            print("Target reached! Please insert the next position")
            x = float(input('x : '))
            y = float(input('y : '))
            rospy.set_param("des_pos_x", x)
            rospy.set_param("des_pos_y", y)
            print("Thanks! Let's make arrangements for some seconds, then reach x = " + str(x) + ", y = " + str(y))
            start_task()
            os.system('clear')
            print("Thanks! Let's make arrangements for some seconds, then reach x = " + str(x) + ", y = " + str(y))
            start_time = datetime.now()

        elif timeout_:
            os.system('clear')
            print("Oh no! Timeout! Please insert another goal")
            x = float(input('x : '))
            y = float(input('y : '))
            rospy.set_param("des_pos_x", x)
            rospy.set_param("des_pos_y", y)
            print("Thanks! Let's make arrangements for some seconds, then reach x = " + str(x) + ", y = " + str(y))
            start_task()
            os.system('clear')
            print("Thanks! Let's make arrangements for some seconds, then reach x = " + str(x) + ", y = " + str(y))
            timeout_ = False
            start_time = datetime.now()

        else:
            continue
        
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass