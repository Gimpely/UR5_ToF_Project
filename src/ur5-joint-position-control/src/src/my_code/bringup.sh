#!/bin/bash
gnome-terminal \
    --window -t 'Gazebo' \
        -- roslaunch gazebo_ros empty_world.launch
        sleep 3
gnome-terminal \
    --window -t 'Spawn robot' \
        -- rosrun gazebo_ros spawn_model -file `rospack find ur5-joint-position-control`/urdf/ur5_jnt_pos_ctrl.urdf.xacro -urdf -x 0 -y 0 -z 0 -model ur5
        sleep 5
gnome-terminal \
    --window -t 'Turn on controller' \
        -- roslaunch ur5-joint-position-control ur5_joint_position_control.launch
        sleep 3
gnome-terminal \
    --window -t 'Turn on RTDE' \
        -- rosrun ur5-joint-position-control active_q.py
        # -- rosrun ur5-joint-position-control aControl_q.py
# # gnome-terminal \
# #     --window -t 'Positions and vel to CSV' \
# #         -- rosrun ur5-joint-position-control pos_vel_2_csv.py



# #simulirani senzorji + zapisovanje v csv
# gnome-terminal \
#     --window -t 'Sim lidar data' \
#         -- roslaunch ur5-joint-position-control lidar_scan_test.launch
#         sleep 2

# #     #realni senzorji + zapisovanje v csv
# gnome-terminal \
#     --window -t 'Real lidar data' \
#         -- python sensor_test_ROS.py
#         sleep 2

# #     #grafi
# gnome-terminal \
#     --window -t 'Publish the diffs' \
#         -- python LiveGraph.py
        


    