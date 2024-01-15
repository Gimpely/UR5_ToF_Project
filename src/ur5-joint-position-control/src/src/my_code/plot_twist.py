#! /usr/bin/env python
import rospy
from std_msgs.msg import Float32, Int32
import matplotlib.pyplot as plt
import threading
from collections import deque

# Create a dictionary to store the data for each topic
data = {}

# Define a callback for each topic that stores the data in the dictionary
def callback(msg, topic):
    if topic not in data:
        data[topic] = deque(maxlen=20)
    data[topic].append(msg.data)

# Define the topics and message types
topicsReal = {
    'sensor/real/A1': Float32,
    'sensor/real/A2': Float32,
    'sensor/real/B1': Float32,
    'sensor/real/B2': Float32,
    'sensor/real/C1': Float32,
    'sensor/real/C2': Float32,
    'sensor/real/D1': Float32,
    'sensor/real/D2': Float32
}

topicsSim = {
    'sensor/A1': Int32,
    'sensor/A2': Int32,
    'sensor/B1': Int32,
    'sensor/B2': Int32,
    'sensor/C1': Int32,
    'sensor/C2': Int32,
    'sensor/D1': Int32,
    'sensor/D2': Int32
}

# Initialize the node
rospy.init_node('listener', anonymous=True)

# Subscribe to each topic
for topics in [topicsReal, topicsSim]:
    for topic, msg_type in topics.items():
        rospy.Subscriber(topic, msg_type, callback, callback_args=topic)

# Create two subplots
fig, axs = plt.subplots(nrows=2, ncols=1)

# Set titles for the subplots
axs[0].set_title('Real')
axs[1].set_title('Sim')

# Update the plots in real time
def update_plots():
    while not rospy.is_shutdown():
        for i, (topic, msg_type) in enumerate(list(topicsReal.items()) + list(topicsSim.items())):
            if topic in data:
                axs[i//8].clear()
                axs[i//8].plot(data[topic])
        plt.pause(0.01)

# Start the plot update in a separate thread
threading.Thread(target=update_plots).start()

# Spin until interrupted
rospy.spin()