from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlebot_patrol',
            executable='patrolMaster',
            name='patrolMaster',
            output='screen'
        ),
        Node(
            package='turtlebot_patrol',
            executable='turnAtObstacle',
            name='turnAtObstacle',
            output='screen'
        ),
        Node(
            package='turtlebot_patrol',
            executable='followLine',
            name='followLine',
            output='screen'
        ),
    ])