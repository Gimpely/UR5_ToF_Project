#! /usr/bin/env python
import numpy as np
import rospy
from sensor_msgs.msg import LaserScan
#from std_msgs.msg import String Float64MultiArray
import time
import csv
import message_filters
import matplotlib.pyplot as plt
import rospkg 
from datetime import datetime
rospack = rospkg.RosPack()
#pub = rospy.Publisher('/lidar_map', Float64MultiArray, queue_size=10)
print('Datas are in meters.')

global time_vec 
global y_var 
time_vec = []
y_var = []
global time_zero
time_zero = float(time.time())
def callback(C1):
    #Goes through all 8 sensors
    data_array = C1
    chess_arranged_arr = []
    
    samples = np.sqrt(np.array(len(data_array.ranges), dtype=np.int))
    samples = np.array(samples, dtype=np.int)
    #print("Samples; ",samples)
    list = []
    array = []
    #Arange data in rows and columns
    
    for j in range(samples):
        i=j*len(data_array.ranges)/samples
        for i in range(i,i+len(data_array.ranges)/samples):        
            list.append(data_array.ranges[i])   
        array.append(list)
        list = []
    arranged_array = arrange_4_4(samples,array)
    array_min = find_min(samples,arranged_array)
    array_min_min = min(array_min)
    write_2_csv(array_min_min)
    y_var.append(array_min)
    
    # print((float(time.time())-time_zero))
    time_vec.append((float(time.time())-time_zero))
    #chess_arranged = np.array(arrange_chess(array_min))
    #talker(chess_arranged)
    
    
#Arange data in 4x4 windows
def arrange_4_4(samples,data):
    arranged_array = []
    for i in range(4):
        for m in range(4):
            for k in range((samples/4)*m,m*samples/4+samples/4):
                for l in range((samples/4)*i,i*samples/4+samples/4):
                    #print("K: ",k,"L: ",l)
                    arranged_array.append(data[k][l])
    #print(len(arranged_array)) #that should be samples^2
    return arranged_array
                
#Find min values in all 16 squares
def find_min(samples,data):
    array = []
    array_min = [] #lenght should be 16
    array_min_heat = []
    for j in range(16):
        for i in range(np.power(samples/4,2)*j,j*np.power(samples/4,2)+np.power((samples/4),2)):
            #print(i)
            array.append(data[i])
        array_min.append(min(array))
        array = []
    #print(array_min)
    return array_min   

#Write to csv - change name
def write_2_csv(data):
    cas = datetime.now()
    with open("/home/student/Desktop/UR_test_ws/src/ur5-joint-position-control/src/src/my_code/lidar_data/lidar_data_C1.csv",'a') as myfile:
        writer = csv.writer(myfile)
        writer.writerow((cas,data))

# def arrange_chess(data):
#     array_min_heat = np.array(np.transpose(np.reshape(data,(4,4))))
#     return array_min_heat

# def animate_heat_map(data,i):
#     plt.imshow(data, cmap='hot', interpolation='nearest')
#     plt.subplot(8, 1, i+1)

def talker(data):
    
    rate = rospy.Rate(100) # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo(data)
        pub.publish(data)
        rate.sleep()
    
    
    

rospy.init_node('lidar_scan')
print('Program starts after 2s.')
time.sleep(2)
time_zero = float(time.time())
C1 = (message_filters.Subscriber('laser_frame_C1', LaserScan))
ts = message_filters.ApproximateTimeSynchronizer([C1], 1, 1)
ts.registerCallback(callback)
print('Writing data to csv file.')

rospy.spin()
# plt.plot(time_vec,y_var)
# plt.legend(['ray 1','ray 2','ray 3','ray 4','ray 5','ray 6','ray 7','ray 8','ray 9','ray 10','ray 11','ray 12','ray 13','ray 14','ray 15','ray 16'])
# plt.xlabel('t [s]') 
# plt.ylabel('Distance [m]')  
# plt.title("Lidar data")
# plt.show()
