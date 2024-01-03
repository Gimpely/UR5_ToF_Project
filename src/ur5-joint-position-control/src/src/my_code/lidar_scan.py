#! /usr/bin/env python
import numpy as np
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32
#from std_msgs.msg import String Float64MultiArray
import time
import csv
import message_filters
import matplotlib.pyplot as plt
import rospkg 
from datetime import datetime


rospack = rospkg.RosPack()
#pub = rospy.Publisher('/lidar_map', Float64MultiArray, queue_size=10)
print('Values in meters.')

pubs = {
    'A1': rospy.Publisher('sensor/A1', Int32, queue_size=10),
    'A2': rospy.Publisher('sensor/A2', Int32, queue_size=10),
    'B1': rospy.Publisher('sensor/B1', Int32, queue_size=10),
    'B2': rospy.Publisher('sensor/B2', Int32, queue_size=10),
    'C1': rospy.Publisher('sensor/C1', Int32, queue_size=10),
    'C2': rospy.Publisher('sensor/C2', Int32, queue_size=10),
    'D1': rospy.Publisher('sensor/D1', Int32, queue_size=10),
    'D2': rospy.Publisher('sensor/D2', Int32, queue_size=10),
}


def callback(A1,A2,B1,B2,C1,C2,D1,D2):
    #Goes through all 8 sensors
    #data_array = [A1,A2,B1,B2,C1,C2,D1,D2]
    data_array = [C1,A1,A2,C2,D2,B2,D1,B1]
    sensor_names = ['C1','A1','A2','C2','D2','B2','D1','B1']
    #data_array = [D1,D1,D1,D1,D1,D1,D1,D1]
    chess_arranged_arr = []

    for l in range(len(data_array)):
        samples = np.sqrt(np.array(len(data_array[l].ranges), dtype=np.int))
        samples = np.array(samples, dtype=np.int)
        
        list = []
        array = []
        #Arange data in rows and columns
        
        for j in range(samples):
            i=j*len(data_array[l].ranges)/samples
            for i in range(i,i+len(data_array[l].ranges)/samples):        
                list.append(data_array[l].ranges[i])   
            array.append(list)
            list = []
        if np.size(array) == 729:
            arranged_array = arrange_4_4(samples,array)
            array_min = find_min(samples,arranged_array)
            
            write_2_csv(min(array_min))
            array_min_min = min(array_min)
            pubs[sensor_names[l]].publish(array_min_min)
            chess_arranged = np.array(arrange_chess(array_min))
            #print('array:',chess_arranged)
            #talker(chess_arranged)
        else: pass
    
  
def mask_outside_circle(data, radius):
    # Ustvarjanje koordinatne mreze
    y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
    
    # Ustvarjanje maske za vrednosti izven kroga
    mask = x**2 + y**2 > radius**2
    
    # Nastavitev vrednosti izven kroga na inf
    data[mask] = np.inf
    
    return data  
    
#Arange data in 4x4 windows
def arrange_4_4(samples,data):
    # print('data: ',np.size(data))
    # print('samples: ',(samples))

    # Preoblikovanje podatkov
    data_reshaped = np.reshape(data, (27, 27))

    # Uporaba maske na preoblikovanih podatkih
    masked_data = mask_outside_circle(data_reshaped, 13)


    # Izris heatmap
    # plt.figure(figsize=(10,10)) # nastavi velikost slike
    # plt.imshow(masked_data, cmap='hot', interpolation='nearest')
    # plt.colorbar() # dodaj barvno skalo
    # plt.title('Heatmap of arranged data')
    # plt.show()
    arranged_array = []
    for i in range(4):
        for m in range(4):
            for k in range((samples/4)*m,m*samples/4+samples/4):
                for l in range((samples/4)*i,i*samples/4+samples/4):
                    #print("K: ",k,"L: ",l)
                    arranged_array.append(masked_data[l][k])
    #print('arranged data',np.size(arranged_array))
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
    with open(rospack.get_path('ur5-joint-position-control')+'/src/src/my_code/lidar_data/lidar_data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((cas,data))

def arrange_chess(data):
    array_min_heat = np.array(np.transpose(np.reshape(data,(4,4))))
    return array_min_heat

def animate_heat_map(data,i):
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.subplot(8, 1, i+1)

def talker(data):
    
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo(data)
        pub.publish(data)
        rate.sleep()
    
    
    

rospy.init_node('lidar_scan')
print('Program starts after 1 s.')
time.sleep(1)
A1 = (message_filters.Subscriber('laser_frame_A1', LaserScan))
A2 = (message_filters.Subscriber('laser_frame_A2', LaserScan))
B1 = (message_filters.Subscriber('laser_frame_B1', LaserScan))
B2 = (message_filters.Subscriber('laser_frame_B2', LaserScan))
C1 = (message_filters.Subscriber('laser_frame_C1', LaserScan))
C2 = (message_filters.Subscriber('laser_frame_C2', LaserScan))
D1 = (message_filters.Subscriber('laser_frame_D1', LaserScan))
D2 = (message_filters.Subscriber('laser_frame_D2', LaserScan))
print(D1)
ts = message_filters.ApproximateTimeSynchronizer([A1,A2,B1,B2,C1,C2,D1,D2], 1, 1)
#ts = message_filters.ApproximateTimeSynchronizer([C1], 1, 1)
ts.registerCallback(callback)
print('Writing data to csv file.')


rospy.spin()