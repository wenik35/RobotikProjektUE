from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlebot_patrol',
            executable='turn',
            name='turn'
        ),
        Node(
            package='turtlebot_patrol',
            executable='patrol',
            name='patrol'
        ),
        Node(
            package='turtlebot_patrol',
            executable='master',
            name='master'
        ),
    ])