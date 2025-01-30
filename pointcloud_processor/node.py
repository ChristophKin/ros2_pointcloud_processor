import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import struct
import numpy as np

class PointCloudModifier(Node):
    def __init__(self):
        super().__init__('pointcloud_modifier')

        # Subscribe to the input PointCloud2 topic
        self.subscription = self.create_subscription(
            PointCloud2,
            '/sensing/lidar/top/points',
            self.pointcloud_callback,
            10
        )

        # Publisher for the modified PointCloud2
        self.publisher = self.create_publisher(PointCloud2, '/sensing/lidar/top/points_processed', 10)

    def pointcloud_callback(self, msg: PointCloud2):
        # Create new fields by adding I, R, and C
        new_fields = list(msg.fields)

        # Define new fields for Intensity, Return type, and Channel
        new_fields.append(PointField(name='intensity', offset=msg.point_step, datatype=PointField.UINT8, count=1))
        new_fields.append(PointField(name='return_type', offset=msg.point_step + 1, datatype=PointField.UINT8, count=1))
        new_fields.append(PointField(name='channel', offset=msg.point_step + 2, datatype=PointField.UINT16, count=1))

        # Update the point step (size of each point)
        new_point_step = msg.point_step + 4  # Added 1 byte for I, 1 byte for R, and 2 bytes for C

        # Prepare new data array
        new_data = bytearray()

        # Unpack the original point cloud data
        for i in range(msg.height * msg.width):
            point_offset = i * msg.point_step
            point_data = msg.data[point_offset: point_offset + msg.point_step]

            # Unpack the XYZ coordinates
            x, y, z = struct.unpack_from('fff', point_data, 0)

            # Pack the original XYZ
            new_data += struct.pack('fff', x, y, z)

            # Add dummy values for Intensity (I), Return type (R), and Channel (C)
            intensity = np.uint8(100)  # intensity value
            return_type = np.uint8(1)  # return type (1 = strongest)
            channel = np.uint16(i%32)     # channel (number running from 0 to 31)

            # Pack the new I, R, C values
            new_data += struct.pack('BBH', intensity, return_type, channel)

        # Create new PointCloud2 message
        new_msg = PointCloud2()
        new_msg.header = msg.header
        new_msg.height = msg.height
        new_msg.width = msg.width
        new_msg.fields = new_fields
        new_msg.is_bigendian = msg.is_bigendian
        new_msg.point_step = new_point_step
        new_msg.row_step = new_point_step * msg.width
        new_msg.data = bytes(new_data)
        new_msg.is_dense = msg.is_dense

        # Publish the modified point cloud
        self.publisher.publish(new_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudModifier()
    print("[INFO]: PointCloudModifier Node running")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
