#) -*- coding: utf-8 -*-

# General
import sys
import copy
import math
import random
import argparse

# ROS
import rospy
import tf
import rospkg
import geometry_msgs.msg
from std_msgs.msg import String
from geometry_msgs.msg import Pose, PoseStamped, Point, Quaternion
from gazebo_msgs.srv import SpawnModel, DeleteModel

# 3Dモデルのパス取得
MODEL_PATH = rospkg.RosPack().get_path('tsuzuki_sim_description') + '/meshes/knuckle/'

#def load_knuckle(pos, idx):
def load_knuckle(pos, ori, idx):
    #pose = Pose(position=Point(x=pos[0], y=pos[1], z=pos[2]), orientation=ori)
    pose = Pose(position=pos, orientation=ori)
    #pose = Pose(position=pos)

    ref_frame = 'world'

    knuckle_xml = ''
    with open (MODEL_PATH + 'knuckle_approximate.urdf', 'r') as knuckle_file:
        knuckle_xml = knuckle_file.read()

    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    try:
        # スポーン実行
        spawn = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
        resp = spawn('knuckle_' + str(idx), knuckle_xml, '/', pose, ref_frame)
        #return resp.success
    except rospy.ServiceException as e:
        rospy.logerr('Spawn URDF service call failed: {0}'.format(e))
        #return

def delete_knuckle(idx):
    rospy.wait_for_service('/gazebo/delete_model')
    try:
        delete = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        resp = delete('knuckle_' + str(idx))
        #return rest.success
    except rospy.ServiceException as e:
        rospy.logerr('Delete Model service call failed: {0}'.format(e))
        #return

def main():
    print('\n*** Start ***')
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', type=int, default=5,
            help='num is the number of knuckles stacked in bulk')
    args = parser.parse_args()

    num = args.num

    for idx in range(0, num):
        pos_x = random.uniform(0.5, 0.7)
        pos_y = random.uniform(-0.1, 0.1)
        pos_z = random.uniform(1.4, 1.6)
    
        rot_x = random.uniform(-math.pi/5, math.pi/5)
        rot_y = random.uniform(-math.pi/5, math.pi/5)
        rot_z = random.uniform(-math.pi/5, math.pi/5)
        q = tf.transformations.quaternion_from_euler(rot_x, rot_y, rot_z)
    
        position = Point(x=pos_x, y=pos_y, z=pos_z)
        orientation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])

        load_knuckle(position, orientation, idx)
        rospy.sleep(0.5)

    rospy.sleep(10.0)

    for idx in range(0, num):
        delete_knuckle(idx)

    print('*** End ***\n')

if __name__=='__main__':
    try:
        rospy.init_node('knuckle_spawn', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass
