Research Track 1 - Assignment 3 - Solution
================================

This is yet another simple and portable robot simulator. The architecture should be able to get the user request, and let the robot execute one of the following behaviors (depending on the user’s input):
1) autonomously reach a x,y coordinate inserted by the user
2) let the user drive the robot with the keyboard
3) let the user drive the robot assisting them to avoid collisions.

Installing and running
----------------------

After you download the workspace just hit,
```bash
$ roslaunch final_assignment overlord.launch opt:=mod2
```
and change the mod as you wish.

Note: for mod1, you can further extend your input by
```bash
$ roslaunch final_assignment overlord.launch opt:=mod1 des_x:=-5.0 des_y:=5.0
```

Structure
---------
Roslaunch file gets user input and starts the needed nodes for the desired mod.
![alt text](https://postimg.cc/0KdPq0X6)

There are 2 nodes to assure communication.
`userinterface` node asks user for input,
`controller` node provides both autonomous movement, and user-input movement.

There is one service.
`service` service has the structure of `char` request and `float32` response. Response is the increase/decrease value to the velocity.

How it works?
---------
Automous moving part is straighforward. As long as there is no obstacle in front, robot keeps moving. When the front distance lowers to a certain distance, robot checks right and left surroundings. Whichever side is the farthest, robots turns toward that direction.

When user inputs a value, userinterface calls the service with the request char. Controller node, checks the request in the service structure, and puts an increment/decrement response into service, and it itself uses it in linear.x velocity assignment, and publishes it into cmd_vel.

Flowchart
---------
![flowchart4.png](https://i.postimg.cc/90sMZxGB/flowchart4.png)](https://postimg.cc/0KdPq0X6)
![alt text](https://i.postimg.cc/90sMZxGB/flowchart4.png)

Problems Faced and Solved
---------
1) Rviz not showing laser-scan outputs (red-lines): It turns out Ubuntu may have some problems with GPU, and if the package has a GPU laser sensor, the output is not read. Some hero on the Internet commented this beautiful words: "You're getting messages, so it's definitely on. Please, try the non-GPU plugin (remove gpu_ everywhere in the sensor definition)." and "the root cause is an incompatibility with the graphics card/driver; what do you have? I also seem to remember having to upgrade to a newer version of Gazebo to get a GPU plugin working correctly, but that may have been specific to a different lidar model. In any case, the choice is yours whether to further pursue the GPU version of this plugin or settle for the CPU version."
Full post is here: https://answers.ros.org/question/370627/cant-see-scan-in-rviz/

2) Rviz not showing map (no map received error): This answer directed me towards the idea that "I should run map_server": https://get-help.robotigniteacademy.com/t/rviz-no-map-received/4721. Then, I went here: http://wiki.ros.org/map_server, which directed me downloading the 'navigation.git' in here: https://github.com/ros-planning/navigation . After catkin_make, I received the following error

```bash
Could not find a package configuration file provided by "tf2_sensor_msgs" with any of the following names:

    tf2_sensor_msgsConfig.cmake
    tf2_sensor_msgs-config.cmake
```

Then I moved on to this answer: https://answers.ros.org/question/305640/cmake-warning-has-occurred/ , which made me think that I am lacking tf2_sensor_msgs, and I should get it using

```bash
$ sudo apt-get install ros-noetic-tf2-sensor-msgs
```
Indeed, after installing that, the problem is solved.

3) Constant spamming on the terminal by 'Warning: TF_REPEATED_DATA ignoring data with redundant timestamp...': This turns out to be an up-to-date issue with the ticket created on here: https://github.com/ros/geometry2/issues/467

4) the rosdep view is empty: call 'sudo rosdep init' and 'rosdep update'
5) Caused missing packages: https://answers.ros.org/question/353082/missing-packages-after-installing-rosdep-based-on-python3-rosdep2-in-noetic/


Improvements
---------
An option to exit a node anytime can be added.
rosclean command can be added.
cancelling a goal mid-time can be added.
