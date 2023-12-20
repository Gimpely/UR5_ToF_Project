#! /usr/bin/env python
import sys
sys.path.append('..')
import time
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import numpy as np
import math
import rospy
from std_msgs.msg import Float64
import csv
from datetime import datetime

def talker():
    # system variables
    updateFrequency = 500
    samplingTime = 600   #sampling time in seconds

    ROBOT_HOST = '192.168.65.244'   # actual robot
    ROBOT_PORT = 30004

    # connect to the robot
    con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
    con.connect()

    # test connection (get controller version)
    cv = con.get_controller_version()

    # subscribe to the desired data
    config = rtde_config.ConfigFile("cfg.xml")
    state_names, state_types = config.get_recipe("state")
    con.send_output_setup(state_names, state_types, frequency = updateFrequency)
    pub1 = rospy.Publisher('/shoulder_pan_joint_position_controller/command', Float64, queue_size=10)
    pub2 = rospy.Publisher('/shoulder_lift_joint_position_controller/command', Float64, queue_size=10)
    pub3 = rospy.Publisher('/elbow_joint_position_controller/command', Float64, queue_size=10)
    pub4 = rospy.Publisher('/wrist_1_joint_position_controller/command', Float64, queue_size=10)
    pub5 = rospy.Publisher('/wrist_2_joint_position_controller/command', Float64, queue_size=10)
    pub6 = rospy.Publisher('/wrist_3_joint_position_controller/command', Float64, queue_size=10)
    
    
    rospy.init_node('talker', anonymous=True)

    # start the data synchronization
    if not con.send_start():
        print("failed to start data transfer")
        sys.exit()
        
    # the meat and potatoes of this script
    ta = []
    qa = []
    doa = []

    timestamp = str(int(time.time()))
    with open('recordings/state.csv', "a") as f:
        f.write("t,q0,q1,q2,q3,q4,q5,do\n") # write header row
        #while keep_running:
        print("Sampling started")
        for i in range(samplingTime):
            for j in range(updateFrequency):
                # receive the current state
                state = con.receive()
                
                if state is None:
                    break;

                t = state.timestamp
                q = state.actual_q
                do = state.actual_digital_output_bits
                #data = '{},{},{},{},{},{}'.format(q[0]*180/math.pi,q[1]*180/math.pi,q[2]*180/math.pi,q[3]*180/math.pi,q[4]*180/math.pi,q[5]*180/math.pi)
                
                data1 = '{}'.format(q[0])
                data2 = '{}'.format(q[1])
                data3 = '{}'.format(q[2])
                data4 = '{}'.format(q[3])
                data5 = '{}'.format(q[4])
                data6 = '{}'.format(q[5])
                #'{}'.format(t),'{}'.format(q[0]),'{}'.format(q[1]),'{}'.format(q[2]),'{}'.format(q[3]),'{}'.format(q[4]),'{}'.format(q[5])
                #print(data1,data2,data3,data4,data5,data6)
                #for i in range(len(q)):
                #    print('Joint {}'.format(i+1)," has value: {}".format(q[i]*180/math.pi))
                
                rate = rospy.Rate(50) # 10hz
            
                data1 = float(data1)
                pub1.publish(data1)
                data2 = float(data2)
                pub2.publish(data2)
                data3 = float(data3)
                pub3.publish(data3)
                data4 = float(data4)
                pub4.publish(data4)
                data5 = float(data5)
                pub5.publish(data5)
                data6 = float(data6)
                pub6.publish(data6)
                writer = csv.writer(f)
                cas = datetime.now()
                writer.writerow((cas,data3,data2,data1,data4,data5,data6))
 # write header row
                rate.sleep()
    con.send_pause()
    con.disconnect()
    

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

