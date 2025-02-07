#! /usr/bin/env python3

import rclpy
import rclpy.logging
from rclpy.node import Node, Publisher
from rclpy.time import Time
import threading


from geometry_msgs.msg import Twist
import rclpy.time

class ForwardYawNode(Node):
    
    twist_pub : Publisher
    logger = None
    
    def __init__(self):
        super().__init__('drive_forward_yaw')
        self.logger = self.get_logger()
        self.twist_pub = self.create_publisher(Twist, "twist_controller", 10)
        # self.drive_forward_yaw()
        
    def drive_forward_yaw(self):
        
        speed = float(input("Enter a speed value: "))
        yaw = float(input("Enter a yaw value: "))
        duration = float(input("Enter the duration in seconds: "))
        
        end = Time(seconds=self.get_clock().now().seconds_nanoseconds()[0] + duration, clock_type=self.get_clock().clock_type)
        twist = Twist()
        twist.linear.x = speed
        twist.angular.z = yaw
        rate = self.create_rate(20, self.get_clock())
        
        while(self.get_clock().now() < end):
            self.twist_pub.publish(twist)
            rate.sleep()
            
            
def main(args=None):
    rclpy.init(args=args)
    node = ForwardYawNode()
    threading.Thread(target=rclpy.spin, args=(node,), daemon=True).start()
    node.drive_forward_yaw()
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()