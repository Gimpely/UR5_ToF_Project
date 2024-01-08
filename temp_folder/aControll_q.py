import rospy
from std_msgs.msg import Float64
from tkinter import *

def talker():
    # system variables
    updateFrequency = 500
    samplingTime = 600   #sampling time in seconds

    pub1 = rospy.Publisher('/shoulder_pan_joint_position_controller/command', Float64, queue_size=10)
    pub2 = rospy.Publisher('/shoulder_lift_joint_position_controller/command', Float64, queue_size=10)
    pub3 = rospy.Publisher('/elbow_joint_position_controller/command', Float64, queue_size=10)
    pub4 = rospy.Publisher('/wrist_1_joint_position_controller/command', Float64, queue_size=10)
    pub5 = rospy.Publisher('/wrist_2_joint_position_controller/command', Float64, queue_size=10)
    pub6 = rospy.Publisher('/wrist_3_joint_position_controller/command', Float64, queue_size=10)
    
    rospy.init_node('talker', anonymous=True)

    # UI for changing joint values
    root = Tk()
    joint_values = [DoubleVar() for _ in range(6)]
    for i in range(6):
        Scale(root, from_=-180, to=180, orient=HORIZONTAL, variable=joint_values[i]).pack()

    def publish_values():
        data1 = joint_values[0].get()
        pub1.publish(data1)
        data2 = joint_values[1].get()
        pub2.publish(data2)
        data3 = joint_values[2].get()
        pub3.publish(data3)
        data4 = joint_values[3].get()
        pub4.publish(data4)
        data5 = joint_values[4].get()
        pub5.publish(data5)
        data6 = joint_values[5].get()
        pub6.publish(data6)

    Button(root, text="Publish", command=publish_values).pack()

    root.mainloop()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass