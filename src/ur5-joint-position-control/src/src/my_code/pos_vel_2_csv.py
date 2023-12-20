#! /usr/bin/env python
import rospy
from sensor_msgs.msg import JointState
import csv
import numpy as np
import time
from datetime import datetime

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.velocity)
    write_2_csv(data)

#Write to csv - change name
def write_2_csv(data):
    names = data.name
    with open('pos.csv', 'a') as file:
        writer = csv.writer(file, names)
        cas = datetime.now()
        writer.writerow((cas,data.position))
    with open('vel.csv', 'a') as file:
        writer = csv.writer(file, names)
        writer.writerow(data.velocity)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/joint_states', JointState, callback)

if __name__ == '__main__':
    listener()
    rospy.spin()

