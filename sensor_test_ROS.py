from threading import Thread
import serial
import os
import rospy
from std_msgs.msg import Int32, Header
from sensor_msgs.msg import Int32Stamped

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
        return None, None
    distance1 = txt_array[1]
    distance2 = txt_array[4]
    if txt_array[2] in ['2', '4', '7']:
        distance1 = 2000
    if txt_array[5] in ['2', '4', '7']:
        distance2 = 2000
    return distance1, distance2

def close_serial(ser):
    ser.close()

def collect_data(arduino_board_port, arduino_board_number, collect_data):
    print("Collecting data...")
    global A1, A2, B1, B2, C1, C2, D1, D2
    ser = open_serial(arduino_board_port)
    while True:
        distance1, distance2 = read_data(ser)
        if distance1 is not None and distance2 is not None:
            if arduino_board_number == 0: 
                msg1 = Int32Stamped()
                msg1.header = Header()
                msg1.header.stamp = rospy.Time.now()
                msg2 = Int32Stamped()
                msg2.header = Header()
                msg2.header.stamp = rospy.Time.now()
                C1 = distance1
                A1 = distance2
                msg1.data = A1
                pub_A1.publish(msg1)
                msg2.data = C1
                pub_C1.publish(msg2)
            if arduino_board_number == 1: 
                msg1 = Int32Stamped()
                msg1.header = Header()
                msg1.header.stamp = rospy.Time.now()
                msg2 = Int32Stamped()
                msg2.header = Header()
                msg2.header.stamp = rospy.Time.now()
                C2 = distance2
                A2 = distance1
                C2 = distance2
                A2 = distance1
                msg1.data = A2
                pub_A2.publish(msg1)
                msg2.data = C2
                pub_C2.publish(msg2)
            if arduino_board_number == 2: 
                msg1 = Int32Stamped()
                msg1.header = Header()
                msg1.header.stamp = rospy.Time.now()
                msg2 = Int32Stamped()
                msg2.header = Header()
                msg2.header.stamp = rospy.Time.now()
                D2 = distance1
                B2 = distance2
                D2 = distance1
                B2 = distance2
                msg1.data = B2
                pub_B2.publish(msg1)
                msg2.data = D2
                pub_D2.publish(msg2)
            if arduino_board_number == 3: 
                msg1 = Int32Stamped()
                msg1.header = Header()
                msg1.header.stamp = rospy.Time.now()
                msg2 = Int32Stamped()
                msg2.header = Header()
                msg2.header.stamp = rospy.Time.now()
                D1 = distance1
                B1 = distance2
                msg1.data = B1
                pub_B1.publish(msg1)
                msg2.data = D1
                pub_D1.publish(msg2)

    close_serial(ser)


def main():
    print("Starting....")
    ARDUINO_BOARD_PORT_ARRAY = ["COM3", "COM4", "COM5", "COM6"]
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
    pub_A1 = rospy.Publisher('A1', Int32Stamped, queue_size=10)
    pub_A2 = rospy.Publisher('A2', Int32Stamped, queue_size=10)
    pub_B1 = rospy.Publisher('B1', Int32Stamped, queue_size=10)
    pub_B2 = rospy.Publisher('B2', Int32Stamped, queue_size=10)
    pub_C1 = rospy.Publisher('C1', Int32Stamped, queue_size=10)
    pub_C2 = rospy.Publisher('C2', Int32Stamped, queue_size=10)
    pub_D1 = rospy.Publisher('D1', Int32Stamped, queue_size=10)
    pub_D2 = rospy.Publisher('D2', Int32Stamped, queue_size=10)
    
    main()
