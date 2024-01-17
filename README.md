# Running the script:
  - `rm -rf build devel`
  - `catkin_make` 
  - `source devel/setup.bash`
  - `cd src/ur5-joint-position-control/src/src/my_code`
or
  - `cd src/tof_project/scripts`
  - `./bringup.sh`

# 1. UR5 Robot Digital Twin Documentation

## 1.1 Overview

This documentation details the setup and configuration for simulating the UR5 robot in a Gazebo environment, integrated with ROS. It includes instructions for automating the launch of various ROS nodes and the simulation environment, as well as the URDF description of the UR5 robot.

## 1.2 Script for Simulation Automation

### 1.2.1 Script Functionality

The script automates the launch of ROS nodes and Gazebo environments essential for the UR5 robot simulation. It utilizes `gnome-terminal` windows to execute different components.

#### 1.2.1.1 Commands Executed

1. **Gazebo Launch**:
   - `roslaunch gazebo_ros empty_world.launch`: Launches an empty Gazebo world.
   - Terminal Title: **Gazebo**

2. **UR5 Robot Model Spawn**:
   - `rosrun gazebo_ros spawn_model -file ur5_jnt_pos_ctrl.urdf.xacro`: Spawns the UR5 robot model in Gazebo. For more details, see the [UR5 Robot Description in URDF](#13-ur5-robot-description-in-urdf).

   - Terminal Title: **Spawn robot**

3. **Joint Position Controller Activation**:
   - `roslaunch ur5_control ur5_jnt_pos_ctrl.launch`: Activates the UR5 joint position controller.
   - Terminal Title: **Turn on controller**

4. **RTDE Node Execution**:
   - `python active_q.py`: Executes the script for Real-Time Data Exchange (RTDE).
   - Terminal Title: **Turn on RTDE**

### 1.2.2 Optional Components

- **Simulated Sensor Data**:
  - For launching simulated LIDAR data. (Commented out)

- **Real Sensor Data Handling**:
  - For processing real LIDAR data via a Python script. (Commented out)

## 1.3 UR5 Robot Description in URDF

### 1.3.1 Robot Definition

- **Name**: `ur5`
- **Format**: Unified Robot Description Format (URDF)

### 1.3.2 Gazebo Plugin Integration

- **Plugin**: `gazebo_ros_control` for ROS control in Gazebo.

### 1.3.3 Robot Links

- **Components**: Includes `base_link`, `shoulder_link`, etc.
- **Properties**:
  - **Visual**: Geometry and materials.
  - **Collision**: Simplified collision geometry.
  - **Inertial**: Mass and inertia matrix.

### 1.3.4 Robot Joints

- **Types**: Primarily `revolute`.
- **Properties**:
  - **Connections**: Links connected by each joint.
  - **Origin**: Position and orientation.
  - **Axis**: Rotation axis.
  - **Limits**: Motion range and constraints.

### 1.3.5 Transmission Elements

- Describes the relationship between joints and actuators.

### 1.3.6 Sensors

- **Types**: Multiple laser sensors (e.g., `laser_frame_D1`).
- **Attachments**: Fixed to parts like `wrist_3_link`.
- **Configurations**: Range, field of view, update rate.
- **Purpose**: Distance measurement, environment scanning.

### 1.3.7 Environment Representation

- **STL File**: `tekociTrak.STL` represents the robot's operational environment.

### 1.3.8 World Integration

- **Global Reference**: Positioning of the robot in the world coordinate system.

This URDF provides a comprehensive representation of the UR5 robot for realistic simulation and control in ROS and Gazebo environments.

