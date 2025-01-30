# ros2_pointcloud_processor
Node Name: PointCloudModifier

This ROS2 node processes 3D point cloud data from a LiDAR sensor. The node performs the following tasks:

1. Subscribes to a PointCloud2 Topic: The node listens to the '/sensing/lidar/top/points topic'.

2. Modifies the Point Cloud Data: Upon receiving a PointCloud2 message, the node:

3. Adds three new fields:
- intensity: An unsigned 8-bit integer representing the intensity of the point (set to a dummy value of 100).
- return_type: An unsigned 8-bit integer representing the type of LiDAR return (set to a dummy value of 1, indicating the strongest return).
- channel: An unsigned 16-bit integer representing the channel (calculated as i % 32 for 32 channels, where i is the point index).

4. Updates the point step: Adjusts the byte size of each point to account for the added fields.

5. Populates the new point cloud data: Copies existing XYZ data and appends the new fields for each point.
6. Publishes the Modified Point Cloud: The modified PointCloud2 messages are published to the /sensing/lidar/top/points_processed topic for further use.

