"""
Following node
"""

import rclpy
import rclpy.context
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from turtlebot_follower.stop import spinUntilKeyboardInterrupt

class turnAtObstacleNode(Node):
    def __init__(self):
        #initialize 
        super().__init__('turnAtObstacle')

        # definition of the parameters that can be changed at runtime
        self.declare_parameter('distance_to_turn', 0.5)
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
        self.publisher_ = self.create_publisher(Twist, 'turnTop', 10)

    def scanner_callback(self, msg):
         # caching the parameters for reasons of clarity
        distance_turn_param = self.get_parameter('distance_to_turn').get_parameter_value().double_value
        speed_param = self.get_parameter('turn_speed').get_parameter_value().double_value

        out = Twist()

        if (not self.active):
            if(0 < msg.ranges[0] < distance_turn_param):
                print("Sending signal to start turning")
                self.active = True
                out.linear.x = 0.0
                out.angular.z = speed_param
                self.publisher_.publish(out)

        else:
            if(0 < msg.ranges[int(len(msg.ranges)/2)] < distance_turn_param):
                print("Sending signal to stop turning")
                self.active = False
                out.angular.z = 0.0
                self.publisher_.publish(out)


def main(args=None):
    spinUntilKeyboardInterrupt(args, turnAtObstacleNode)

if __name__ == '__main__':
    main()
