#!/usr/bin/env python
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QPushButton, QLabel
import rospy
from std_msgs.msg import Float64

class JointController(QWidget):
    def __init__(self):
        super(JointController, self).__init__()

        # ROS setup (add your ROS publishers here)
        self.init_ros()

        # Create sliders for each joint
        self.sliders = []
        self.create_sliders()

        # Publish button
        self.publish_button = QPushButton("Publish")
        self.publish_button.clicked.connect(self.publish_values)

        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_application)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.publish_button)
        for label, slider in self.sliders:
            layout.addWidget(label)
            layout.addWidget(slider)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

    def init_ros(self):
        # Initialize ROS node and publishers
        rospy.init_node('joint_controller', anonymous=True)
        # Add your ROS publishers here
        self.pub1 = rospy.Publisher('/shoulder_pan_joint_position_controller/command', Float64, queue_size=10)
        self.pub2 = rospy.Publisher('/shoulder_lift_joint_position_controller/command', Float64, queue_size=10)
        self.pub3 = rospy.Publisher('/elbow_joint_position_controller/command', Float64, queue_size=10)
        self.pub4 = rospy.Publisher('/wrist_1_joint_position_controller/command', Float64, queue_size=10)
        self.pub5 = rospy.Publisher('/wrist_2_joint_position_controller/command', Float64, queue_size=10)
        self.pub6 = rospy.Publisher('/wrist_3_joint_position_controller/command', Float64, queue_size=10)

    def create_sliders(self):
        topic_names = ["/shoulder_pan", "/shoulder_lift", "/elbow", "/wrist_1", "/wrist_2", "/wrist_3"]
        pubs = [self.pub1, self.pub2, self.pub3, self.pub4, self.pub5, self.pub6]

        for i, (topic, pub) in enumerate(zip(topic_names, pubs)):
            slider = QSlider()
            slider.setOrientation(1)  # Vertical orientation
            slider.setMinimum(-180)
            slider.setMaximum(180)
            label = QLabel("Joint {}: {}".format(i+1, topic))  # Label to show joint number and topic name
            self.sliders.append((label, slider))  # Tuple containing label and slider

    def publish_values(self):
        # Publish joint values to ROS
        for i, (label, slider) in enumerate(self.sliders):
            joint_value = slider.value()
            pubs = [self.pub1, self.pub2, self.pub3, self.pub4, self.pub5, self.pub6]
            pubs[i].publish(joint_value)
            rospy.loginfo("Joint {}: Topic: {}, Value: {}".format(i+1, pubs[i].name, joint_value))

    def close_application(self):
        # Close the ROS node and exit the application
        rospy.signal_shutdown("Closing application")
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JointController()
    window.show()
    sys.exit(app.exec_())
