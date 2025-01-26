"""
Following node
"""

import sys
import rclpy
import rclpy.context
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class turnAtObstacleNode(Node):
    def __init__(self):
        #initialize 
        super().__init__('turner')

        # definition of the parameters that can be changed at runtime
        self.declare_parameter('distance_to_turn', 1.0)
        self.declare_parameter('turn_speed', 1.0)
        self.active = False

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
        self.publisher_ = self.create_publisher(Twist, 'patrol_turn', 10)

    def scanner_callback(self, msg):
         # caching the parameters for reasons of clarity
        distance_turn_param = self.get_parameter('distance_to_turn').get_parameter_value().double_value
        speed_param = self.get_parameter('distance_to_turn').get_parameter_value().double_value

        if (not self.active):
            if(msg.ranges[0] < distance_turn_param):
                self.active = True
                self.publisher_
        else:
            out = Twist()

            if(msg.ranges[len(msg.ranges)/2] < distance_turn_param):
                out.angular.z = 0
            else:
                out.angular.z = speed_param
        
            self.publisher_.publish(out)

def main(args=None):
    rclpy.init(args=args)

    follower = turnAtObstacleNode()
    rclpy.spin(follower)

    follower.destroy_node()
    rclpy.shutdown()
    sys.exit(0)

if __name__ == '__main__':
    main()
