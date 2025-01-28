"""
Following node
"""

import rclpy
import rclpy.context
from rclpy.node import Node

from geometry_msgs.msg import Twist

from turtlebot_follower.stop import spinUntilKeyboardInterrupt

class patrolMasterNode(Node):
    def __init__(self):
        #initialize 
        super().__init__('patrolMasterNode')

        # setup laserscanner subscription
        qos_policy = rclpy.qos.QoSProfile(
            reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
            history=rclpy.qos.HistoryPolicy.KEEP_LAST,
            depth=1)
        
        self.follower = self.create_subscription(
            Twist,
            'followLineTop',
            self.follower_callback,
            qos_profile=qos_policy)
        
        self.turner = self.create_subscription(
            Twist,
            'turnTop',
            self.turner_callback,
            qos_profile=qos_policy)
        
        self.follower  # prevent unused variable warning
        self.turner
        self.isTurning = False

        # publisher for driving commands
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

    def follower_callback(self, msg):
        print("Follower callback")
        if(not self.isTurning):
            print("Following line")
            self.publisher_.publish(msg)

    def turner_callback(self, msg):
        print("Turner callback")
        if(msg.angular.z == 0):
            self.isTurning = False
            print("Stopping turn")
        else:
            print("Turning")
            self.isTurning = True
            self.publisher_.publish(msg)

def main(args=None):
    spinUntilKeyboardInterrupt(args, patrolMasterNode)

if __name__ == '__main__':
    main()
