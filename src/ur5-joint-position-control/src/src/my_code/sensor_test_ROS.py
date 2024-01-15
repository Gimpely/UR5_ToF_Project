#!/usr/bin/env python

from threading import Thread
import serial
import os
import rospy
from std_msgs.msg import Int32, Header, Float32
import csv
import rospkg 
import math
from datetime import datetime

A1, A2, B1, B2, C1, C2, D1, D2 = 0, 0, 0, 0, 0, 0, 0, 0

rospack = rospkg.RosPack()

def open_serial(port, baudrate=115200):
    ser = serial.Serial()
    ser.baudrate = baudrate
    ser.port = port
    ser.open()
    return ser

def read_data(ser):
    ser.write(str.encode("\n"))
    txt_array = ser.readline().decode("utf-8").strip().split(",")
   
    if len(txt_array) < 6:
        return None, None, False, False
    distance1 = txt_array[1]
    distance2 = txt_array[4]
    d1_flag = False
    d2_flag = False
    if txt_array[2] in ['2', '2', '2']:
        # if int(distance1) > 200 or int(distance1) < 200:
        # distance1 = float('inf')
        d1_flag = True
    if txt_array[5] in ['2', '2', '2']:
        d2_flag = True
        # if int(distance2) > 200 or int(distance2) < 200:
        # distance2 = float('inf')
    return distance1, distance2, d1_flag, d2_flag

def close_serial(ser):
    ser.close()

# def write_to_csv(filename, A1, A2, B1, B2, C1, C2, D1, D2):
#     with open(filename, 'a') as file:
#         writer = csv.writer(file)
#         writer.writerow([datetime.now(), A1, A2, B1, B2, C1, C2, D1, D2])
def write_to_csv(A1, A2, B1, B2, C1, C2, D1, D2):
    filename = rospack.get_path('ur5-joint-position-control')+'/src/src/my_code/lidar_data/measured_data.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D1', 'D2'])
        writer.writerow([datetime.now(), A1, A2, B1, B2, C1, C2, D1, D2])

def collect_data(arduino_board_port, arduino_board_number, collect_data):
    print("Collecting data...")
    global A1, A2, B1, B2, C1, C2, D1, D2
    with serial.Serial(port=arduino_board_port, baudrate=115200) as ser:
        while True:
            distance1, distance2, f1, f2 = read_data(ser)
            if distance1 is not None and distance2 is not None:
                distance1 = int(distance1)
                distance2 = int(distance2)
                if arduino_board_number == 0: 
                    C1 = distance1
                    A1 = distance2
                    if f1:
                        C1 = float('inf')
                    if f2:
                        A1 = float('inf')
                    pub_A1.publish(A1)
                    pub_C1.publish(C1)
                if arduino_board_number == 1: 
                    C2 = distance2
                    A2 = distance1
                    if f1:
                        A2 = float('inf')
                    if f2:
                        C2 = float('inf')
                    pub_A2.publish(A2)
                    pub_C2.publish(C2)
                if arduino_board_number == 2: 
                    D2 = distance1
                    B2 = distance2
                    if f1:
                        D2 = float('inf')
                    if f2:
                        B2 = float('inf')
                    pub_B2.publish(B2)
                    pub_D2.publish(D2)
                if arduino_board_number == 3:
                    D1 = distance1
                    B1 = distance2
                    if f1:
                        D1 = float('inf')
                    if f2:
                        B1 = float('inf')
                    pub_B1.publish(B1)
                    pub_D1.publish(D1)
                write_to_csv(A1, A2, B1, B2, C1, C2, D1, D2)

        close_serial(ser)


def main():
    print("Starting....")
    ARDUINO_BOARD_PORT_ARRAY = ["/dev/ttyUSB0","/dev/ttyUSB1","/dev/ttyUSB2","/dev/ttyUSB3" ]
    # ARDUINO_BOARD_PORT_ARRAY = ["/dev/ttyUSB2","/dev/ttyUSB3","/dev/ttyUSB4","/dev/ttyUSB5" ]
    # ARDUINO_BOARD_PORT_ARRAY = ["/dev/ttyUSB0" ]
    # ARDUINO_BOARD_PORT_ARRAY = ["/dev/ttyUSB1" ]
    # ARDUINO_BOARD_PORT_ARRAY = ["/dev/ttyUSB2" ]
    # ARDUINO_BOARD_PORT_ARRAY = ["/dev/ttyUSB3" ]

    collect_data_flag = True
    threads = []
    for i, port in enumerate(ARDUINO_BOARD_PORT_ARRAY):
        thread = Thread(target=collect_data, args=[port, i, collect_data_flag])
        thread.start()
        threads.append(thread)
    # Do other stuff
    # When done, stop the threads
    collect_data_flag = False
    for thread in threads:
        thread.join()



if __name__ == "__main__":
    print("Init..")

    rospy.init_node('arduino_data_publisher')

    # Create ROS publishers
    pub_A1 = rospy.Publisher('sensor/real/A1', Float32, queue_size=2)
    pub_A2 = rospy.Publisher('sensor/real/A2', Float32, queue_size=2)
    pub_B1 = rospy.Publisher('sensor/real/B1', Float32, queue_size=2)
    pub_B2 = rospy.Publisher('sensor/real/B2', Float32, queue_size=2)
    pub_C1 = rospy.Publisher('sensor/real/C1', Float32, queue_size=2)
    pub_C2 = rospy.Publisher('sensor/real/C2', Float32, queue_size=2)
    pub_D1 = rospy.Publisher('sensor/real/D1', Float32, queue_size=2)
    pub_D2 = rospy.Publisher('sensor/real/D2', Float32, queue_size=2)
    
    main()