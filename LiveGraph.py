import rospy
from std_msgs.msg import Float32
import matplotlib.pyplot as plt
import threading

# Create lists to hold the data from each topic
data_real = {f"A{i}": [] for i in range(1, 3)} | {f"B{i}": [] for i in range(1, 3)} | {f"C{i}": [] for i in range(1, 3)} | {f"D{i}": [] for i in range(1, 3)}
data_sim = {f"A{i}": [] for i in range(1, 3)} | {f"B{i}": [] for i in range(1, 3)} | {f"C{i}": [] for i in range(1, 3)} | {f"D{i}": [] for i in range(1, 3)}

# Callback functions for each topic
def make_callback(container):
    def callback(msg):
        container.append(msg.data)
    return callback

# Initialize the node
rospy.init_node('listener', anonymous=True)

# Subscribe to the topics
for sensor in data_real.keys():
    rospy.Subscriber(f'sensor/real/{sensor}', Float32, make_callback(data_real[sensor]))
    rospy.Subscriber(f'sensor/{sensor}', Float32, make_callback(data_sim[sensor]))

# Function to update the plot
def update_plot():
    plt.ion()  # Turn on interactive mode
    num_points = 20
    while not rospy.is_shutdown():
        for i, sensor in enumerate(data_real.keys(), start=1):
            plt.subplot(4, 2, i)  # Adjust as needed
            plt.clf()  # Clear the current figure
            if len(data_real[sensor]) > 0 and len(data_sim[sensor]) > 0:
                plt.plot([real - sim for real, sim in zip(data_real[sensor][-num_points:], data_sim[sensor][-num_points:])], label=f'{sensor} Difference')
                plt.legend()
        plt.pause(0.01)  # Pause for a short period to allow the plot to update

# Start the plot update function in a separate thread
plot_thread = threading.Thread(target=update_plot)
plot_thread.start()

# Spin until interrupted
rospy.spin()
