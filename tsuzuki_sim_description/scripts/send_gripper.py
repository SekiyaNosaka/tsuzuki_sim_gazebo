# -*- coding: utf-8 -*-

import argparse

import rospy
import actionlib
import control_msgs.msg

def gripper_client(val):
    client = actionlib.SimpleActionClient('/gripper_controller/gripper_cmd',
            control_msgs.msg.GripperCommandAction)
    client.wait_for_server()

    goal = control_msgs.msg.GripperCommandGoal()
    goal.command.position = val # value range [0.0~0.8]
    goal.command.max_effort = -1.0 # don't limit the effort

    client.send_goal(goal)
    client.wait_for_result()

    return client.get_result()

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--value', type=float, default='0.4',
                help='Value between 0.0 (open) and 0.8 (closed)')
        args = parser.parse_args()
        gripper_value = args.value

        rospy.init_node('send_gripper')

        result = gripper_client(gripper_value)
        print(result)
    except rospy.ROSInterruptException:
        pass
