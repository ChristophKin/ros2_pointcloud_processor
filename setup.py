from setuptools import find_packages, setup

package_name = 'pointcloud_processor'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(include=[package_name]),
    data_files=[
        ('share/ament_index/resource_index/packsages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Christoph Kinberger',
    maintainer_email='christoph.Kinberger@v2c2.at',
    description='ROS2 PointCloud2 processing node',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'pointcloud_modifier = pointcloud_processor.node:main',
        ],
    },
)
