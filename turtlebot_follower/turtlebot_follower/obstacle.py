"""
Following node
"""

import math
import sys

import rclpy
import rclpy.context
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class stopDrivingNode(Node):
    def __init__(self):
        super().__init__('stop')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)

        print("sent stop command")

class followObstacleNode(Node):
    def __init__(self):
        #initialize 
        super().__init__('follower')

        # definition of the parameters that can be changed at runtime
        self.declare_parameter('distance_to_slow_down', 1.0)
        self.declare_parameter('distance_to_stop', 0.3)
        self.declare_parameter('speed_slow', 0.1)
        self.declare_parameter('speed_fast', 0.15)
        self.declare_parameter('speed_slow_turn', 0.4)
        self.declare_parameter('speed_fast_turn', 0.8)
        self.declare_parameter('window', 45)
        self.declare_parameter('debug', False)

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
        window_param = self.get_parameter('window').get_parameter_value().integer_value
        debug = self.get_parameter('debug').get_parameter_value().bool_value

        # finding measurement of nearest obstacle
        nearest_value_index = 0
        nearest_obstacle_distance = 5
        for i in range(0, len(msg.ranges)):
            nearest_obstacle_angle = int(math.degrees(i * msg.angle_increment))

            if (0 < msg.ranges[i] < nearest_obstacle_distance):
                nearest_obstacle_angle = int(math.degrees(i * msg.angle_increment))
                if (not window_param < nearest_obstacle_angle < 360-window_param):
                    nearest_obstacle_distance = msg.ranges[i]
                    nearest_value_index = i

        # calculate helper values
        nearest_obstacle_angle = int(math.degrees(nearest_value_index * msg.angle_increment))
        angle_normalized = nearest_obstacle_angle if nearest_obstacle_angle < 180 else (360 - nearest_obstacle_angle) * -1

        print(f'Nearest obstacle at {angle_normalized} degrees, {nearest_obstacle_distance} m out')

        turn = 0.0
        speed = 0.0

        if (abs(angle_normalized) in range(45, 180)):
            turn = math.copysign(speed_fast_turn_param, angle_normalized)
            print(f'Turning fast with {turn} speed')
        else:
            if (nearest_obstacle_distance > distance_slow_param):
                speed = speed_fast_param
                print("drive fast")
            elif (nearest_obstacle_distance > distance_stop_param):
                speed = speed_slow_param
                print("drive slow")
            else:
                print("stop")
            
            if(angle_normalized != 0):
                turn = speed_slow_turn_param * (angle_normalized / 20)

        # create message
        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = turn

        # send message
        if(not debug):
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    followNode = followObstacleNode()

    try:
        rclpy.spin(followNode)

    except KeyboardInterrupt:
        stopNode = stopDrivingNode()

        followNode.destroy_node()
        stopNode.destroy_node()

        rclpy.shutdown()
        sys.exit(0)

if __name__ == '__main__':
    main()
