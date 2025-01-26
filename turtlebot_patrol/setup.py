from setuptools import find_packages, setup
import os
import glob

package_name = 'turtlebot_patrol'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml', 'launch/patrol_launch.py']),
    
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nik',
    maintainer_email='niwer0305@gmx.de',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turn = turtlebot_patrol.obstacle:main',
            'patrol = turtlebot_patrol.line:main',
            'master = turtlebot_patrol.master:main'
        ],
    },
)
