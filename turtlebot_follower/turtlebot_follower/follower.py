"""
Following node
"""

import numpy as np

import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Float32
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import datetime


class followObstacleNode(Node):

    def __init__(self):
        #initialize 
        super().__init__('follower')

        # definition of the parameters that can be changed at runtime
        self.declare_parameter('distance_to_slow_down', 1.0)
        self.declare_parameter('distance_to_stop', 0.3)
        self.declare_parameter('speed_slow', 0.1)
        self.declare_parameter('speed_fast', 0.15)
        self.declare_parameter('speed_slow_turn', 0.2)
        self.declare_parameter('speed_fast_turn', 0.4)

        # setup laserscanner subscription
        qos_policy = rclpy.qos.QoSProfile(
            reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
            history=rclpy.qos.HistoryPolicy.KEEP_LAST,
            depth=1)
        
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scanner_callback,
            qos_profile=qos_policy)
        self.subscription  # prevent unused variable warning

        # publisher for driving commands
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

    def scanner_callback(self, msg):
         # caching the parameters for reasons of clarity
        distance_slow_param = self.get_parameter('distance_to_slow_down').get_parameter_value().double_value
        distance_stop_param = self.get_parameter('distance_to_stop').get_parameter_value().double_value
        speed_slow_param = self.get_parameter('speed_slow').get_parameter_value().double_value
        speed_fast_param = self.get_parameter('speed_fast').get_parameter_value().double_value
        speed_slow_turn_param = self.get_parameter('speed_slow_turn').get_parameter_value().double_value
        speed_fast_turn_param = self.get_parameter('speed_fast_turn').get_parameter_value().double_value

        # finding angle of nearest obstacle
        nearest_obstacle_distance = msg.min_range
        nearest_obstacle_angle = np.argmin(np.array(msg.ranges)) * msg.angle_increment
        nearest_obstacle_angle_deg_int = int(np.rad2deg(nearest_obstacle_angle)[0])
        angle_normalized = (nearest_obstacle_angle_deg_int - 180) * -1
        angle_normalized_absolute = np.abs(angle_normalized)

        if (angle_normalized_absolute in range(90, 180)):
            speed = 0.0
            if (angle_normalized > 0):
                turn = speed_fast_turn_param
                print("turn right fast")
            else:
                turn = speed_fast_turn_param * -1
                print("turn left fast")

        else:
            if (nearest_obstacle_distance > distance_slow_param):
                speed = speed_fast_param
                print("drive fast")
            elif (nearest_obstacle_distance > distance_stop_param):
                speed = speed_slow_param
                print("drive slow")
            else:
                speed = 0.0
                print("stop")
            
            if(angle_normalized_absolute > 10):
                turn = speed_slow_turn_param * (angle_normalized / 100)

        # create message
        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = turn

        # send message
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    followNode = followObstacleNode()

    rclpy.spin(followNode)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    followNode.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
