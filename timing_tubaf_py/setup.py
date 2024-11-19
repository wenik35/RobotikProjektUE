from setuptools import find_packages, setup

package_name = 'timing_tubaf_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Niklas',
    maintainer_email='niwer0305@gmx.de',
    description='Übungs-Package für Robotik-Projekt',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'example_node = timing_tubaf_py.example_node:main',
            'listener = timing_tubaf_py.pubsub_member_function:main',
        ],
    },
)
