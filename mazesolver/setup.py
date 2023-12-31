from setuptools import find_packages, setup

package_name = 'mazesolver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        #('share/' + package_name, ['maze_objs/WholeMaze.stl'])

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='laurent',
    maintainer_email='lthorbecke11@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'wall_follower = mazesolver.wall_follower:main',
            'follow_path_lidar = mazesolver.follow_path_lidar:main',
        ],
    },
)
