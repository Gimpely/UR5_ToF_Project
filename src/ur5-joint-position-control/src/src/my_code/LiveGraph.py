#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
import csv
from datetime import datetime

# Dictionary to store data for each topic
data_real = {'B1': None, 'B2': None, 'D1': None, 'D2': None}
data_sim = {'B1': None, 'B2': None, 'D1': None, 'D2': None}



# File path for CSV
csv_file_path = '/home/student/Desktop/UR_test_ws/src/ur5-joint-position-control/src/src/my_code/lidar_data/differences.csv'  # Change this to the desired path

# Initialize the node
rospy.init_node('difference_calculator', anonymous=True)

# Publishers for differences
pub_difference_B1 = rospy.Publisher('sensor/diff/B1', Float32, queue_size=10)
pub_difference_B2 = rospy.Publisher('sensor/diff/B2', Float32, queue_size=10)
pub_difference_D1 = rospy.Publisher('sensor/diff/D1', Float32, queue_size=10)
pub_difference_D2 = rospy.Publisher('sensor/diff/D2', Float32, queue_size=10)

# Callback for real topics
def callback_real(msg, topic):
    global data_real
    data_real[topic] = msg.data

# Callback for simulated topics
def callback_sim(msg, topic):
    global data_sim
    data_sim[topic] = msg.data

# Subscribe to real topics
rospy.Subscriber('sensor/real/B1', Float32, callback_real, callback_args='B1')
rospy.Subscriber('sensor/real/B2', Float32, callback_real, callback_args='B2')
rospy.Subscriber('sensor/real/D1', Float32, callback_real, callback_args='D1')
rospy.Subscriber('sensor/real/D2', Float32, callback_real, callback_args='D2')

# Subscribe to simulated topics
rospy.Subscriber('sensor/B1', Float32, callback_sim, callback_args='B1')
rospy.Subscriber('sensor/B2', Float32, callback_sim, callback_args='B2')
rospy.Subscriber('sensor/D1', Float32, callback_sim, callback_args='D1')
rospy.Subscriber('sensor/D2', Float32, callback_sim, callback_args='D2')

# Open the CSV file for writing with header
with open(csv_file_path, 'w') as csv_file:
    fieldnames = ['Timestamp', 'B1', 'B2', 'D1', 'D2']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header
    csv_writer.writeheader()

    # Update the differences and publish them in real-time
    rate = rospy.Rate(38)  # Adjust the rate as needed
    while not rospy.is_shutdown():
        if all(data_real.values()) and all(data_sim.values()):
            latest_real = {key: value for key, value in data_real.items()}
            latest_sim = {key: value for key, value in data_sim.items()}
            
            difference_B1 = latest_real['B1'] - 1000 * latest_sim['B1']
            difference_B2 = latest_real['B2'] - 1000 * latest_sim['B2']
            difference_D1 = latest_real['D1'] - 1000 * latest_sim['D1']
            difference_D2 = latest_real['D2'] - 1000 * latest_sim['D2']

            # Publish differences
            pub_difference_B1.publish(Float32(difference_B1))
            pub_difference_B2.publish(Float32(difference_B2))
            pub_difference_D1.publish(Float32(difference_D1))
            pub_difference_D2.publish(Float32(difference_D2))

            # Get the current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            # Write the differences to the CSV file
            csv_writer.writerow({'Timestamp': timestamp, 'B1': difference_B1, 'B2': difference_B2, 'D1': difference_D1, 'D2': difference_D2})

            # Uncomment the line below if you want to log the differences to console
            # rospy.loginfo("Published differences: B1={}, B2={}, D1={}, D2={}".format(difference_B1, difference_B2, difference_D1, difference_D2))

        rate.sleep()
