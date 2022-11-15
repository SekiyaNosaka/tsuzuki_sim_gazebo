# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Header
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

def main():
    pub = rospy.Publisher('/manipulator_controller/command', JointTrajectory, queue_size=10)

    traj = JointTrajectory()
    traj.header = Header()
    traj.joint_names = ['shoulder_pan_joint',
                        'shoulder_lift_joint',
                        'elbow_joint',
                        'wrist_1_joint',
                        'wrist_2_joint',
                        'wrist_3_joint']

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        traj.header.stamp = rospy.Time.now()
        
        pts = JointTrajectoryPoint()
        pts.positions = [0.0, -2.33, 1.57, 0.0, 0.0, 0.0]
        pts.time_from_start = rospy.Duration(1.0)
        
        traj.points = []
        traj.points.append(pts)

        pub.publish(traj)

if __name__ == '__main__':
    try:
        rospy.init_node('send_joints')
        main()
    except rospy.ROSInterruptException:
        pass
