Research Track 1 - Assignment 3 - Solution
================================

This is yet another simple and portable robot simulator. The architecture should be able to get the user request, and let the robot execute one of the following behaviors (depending on the user’s input):
1) autonomously reach a x,y coordinate inserted by the user
2) let the user drive the robot with the keyboard
3) let the user drive the robot assisting them to avoid collisions.

Installing and running
----------------------

After you download the workspace for the following desired mods, just hit,

Mod1: autonomously reach a x,y coordinate inserted by the user
```bash
$ roslaunch final_assignment overlord.launch opt:=mod1 des_x:=-5.0 des_y:=5.0
```

Mod2: let the user drive the robot with the keyboard
```bash
$ roslaunch final_assignment overlord.launch opt:=mod2
```

Mod3: let the user drive the robot assisting them to avoid collisions.
```bash
$ roslaunch final_assignment overlord.launch opt:=mod2
```

Structure and How it works
---------
Roslaunch file gets user input mod and starts the needed nodes for the desired mod.

Mod1 starts an initializer node, which then calls for another node through roslaunch to send user input goals to move_base/goal topic.

Mod2 calls for teleopt_twist_keyboard to take user direction inputs.

Mod3 calls for a modified version teleopt_twist_keyboard(to publish on /cmd_vel_**raw**) to take user direction inputs, and calls another node to manipulate user inputs when user feels like crashing into a wall.

Flowchart
---------
![flowchart6](https://user-images.githubusercontent.com/71343894/154901294-0254529a-75bb-448d-a042-693fac1bd328.png)


Improvements
---------
1) Cancelling a goal mid-time can be added. 
3) An option to exit a node anytime can be added.
4) rosclean command can be added if user has a huge size of .ros/log initially.


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


