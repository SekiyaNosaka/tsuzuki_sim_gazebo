# -*- coding: utf-8 -*- 

# General
import cv2
import numpy as np
import matplotlib.pyplot as plt

# ROS
import rospy
import rospkg
import tf
import sensor_msgs.point_cloud2 as pc2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, PointCloud2

class Test():
    def __init__(self):
        # common
        self.cv_bridge = CvBridge()
        # Color Callback
        self.c_img = []
        # Depth Callback
        self.d_img = []
        # PointCloud Callback
        self.pcd_x = [] 
        self.pcd_y = []
        self.pcd_z = []
        self.pcd_width = 0
        self.pcd_height = 0
        # sub
        rospy.wait_for_message('/n35/color/image_raw', Image)
        rospy.wait_for_message('/n35/depth/image_raw', Image)
        rospy.wait_for_message('/n35/depth/points', PointCloud2)
        #rospy.Subscriber('/n35/color/image_raw', Image, self.color_CB, queue_size=1)
        rospy.Subscriber('/n35/depth/image_raw', Image, self.depth_CB, queue_size=1)
        #rospy.Subscriber('/n35/depth/points', PointCloud2, self.pointcloud_CB, queue_size=1)

    def color_CB(self, msg):
        try:
            self.c_img = self.cv_bridge.imgmsg_to_cv2(msg)
            #print(self.c_img.shape)
        except CvBridgeError as e:
            rospy.loginfo(e)

    def depth_CB(self, msg):
        try:
            self.d_img = self.cv_bridge.imgmsg_to_cv2(msg)
            print(self.d_img.shape) # MEMO: (h:1024, w:1280) self.d_img[h][w] or self.d_img[h, w]

            # 切り取り加工しまっせ〜
            cut_size_h = 250
            cut_size_w = 250
            cut_left_edge_h = 0
            cut_left_edge_w = 1030
            cut_img_center_h = cut_left_edge_h + 124
            cut_img_center_w = cut_left_edge_w + 124
            cut_d_img = self.d_img[cut_left_edge_h:cut_left_edge_h+250, cut_left_edge_w:cut_left_edge_w+250]
            print(cut_d_img.shape)
            plt.imshow(cut_d_img)
            plt.show()

        except CvBridgeError as e:
            rospy.loginfo(e)

    def pointcloud_CB(self, msg):
        pcd_x = []
        pcd_y = []
        pcd_z = []

        for p in pc2.read_points(msg):
            pcd_x.append(p[0]) 
            pcd_y.append(p[1])
            pcd_z.append(p[2])

        self.pcd_x = pcd_x
        self.pcd_y = pcd_y
        self.pcd_z = pcd_z
        self.pcd_width  = msg.width
        self.pcd_height = msg.height

        pcd_x_re = np.array(self.pcd_x).reshape(1024, 1280)
        pcd_y_re = np.array(self.pcd_y).reshape(1024, 1280)
        pcd_z_re = np.array(self.pcd_z).reshape(1024, 1280)
        #print((pcd_x_re.shape, pcd_y_re.shape, pcd_z_re.shape))

if __name__ == "__main__":
    try:
        rospy.init_node('check_test', anonymous=True)
        test = Test()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
