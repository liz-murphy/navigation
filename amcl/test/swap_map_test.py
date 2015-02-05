#!/usr/bin/env python

import rospy
import nav_msgs
import mapper
import os
from geometry_msgs.msg import Pose

class TestSwapMap:
    def __init__(self):
        self.mode = 0;
        self.pub = rospy.Publisher('received_map', nav_msgs.msg.OccupancyGrid, queue_size=1)
        rospy.loginfo("Waiting for service ...")
        rospy.wait_for_service('set_map')
        rospy.loginfo("Service up ervice ...")

    def swap(self):
        swap_maps = rospy.ServiceProxy('set_map', nav_msgs.srv.SetMap)
        if self.mode == 0:
            new_map = mapper.loadMapFromFile(os.getcwd() + '/maps/1/map.yaml')
            self.pub.publish(new_map.map)
            new_pose = Pose()
            new_pose.position.x = 10.0
            new_pose.orientation.w = 1.0
            print new_pose
            resp = swap_maps(new_map.map, new_pose)
            print resp
            self.mode = 1
        else:
            new_map = mapper.loadMapFromFile(os.getcwd() + '/maps/2/map.yaml')
            self.pub.publish(new_map.map)
            new_pose = Pose()
            new_pose.position.y = 10.0
            new_pose.orientation.w = 1.0
            resp = swap_maps(new_map.map, new_pose)
            print resp
            self.mode = 0


if __name__ == '__main__':
    rospy.init_node('swap_map_test', anonymous=True)
    test_swap = TestSwapMap()
    rate = rospy.Rate(0.1) # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo("Swapping")
        test_swap.swap()
        rate.sleep()
