#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
import math
class TurtleCircleDrawer(Node):
    def __init__(self):
        super().__init__('turtle_circle_drawer')
        self.turtle1_x = 5.0
        self.turtle1_y = 5.0
        self.turtle2_x = 5.0
        self.turtle2_y = 5.0
        self.turtle1_ready = False
        self.spawn_client = self.create_client(Spawn, 'spawn')
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Spawn service not available, waiting...')
        self.spawn_request = Spawn.Request()
        self.create_timer(1.0, self.spawn_head_turtle)
    def spawn_head_turtle(self):
        self.spawn_request.x = self.turtle1_x
        self.spawn_request.y = self.turtle1_y
        self.spawn_request.theta = 0.0
        self.spawn_request.name = "head_turtle"
        self.spawn_turtle(self.spawn_request, self.draw_head_circle)
    def draw_head_circle(self, future):
        self.draw_circle("head_turtle", 1.0, self.stop_head_turtle)
    def stop_head_turtle(self):
        self.stop_turtle("head_turtle")
        self.turtle1_ready = True
        self.spawn_body_turtle()
    def spawn_body_turtle(self):
        if self.turtle1_ready:
            self.spawn_request.x = self.turtle2_x
            self.spawn_request.y = self.turtle2_y
            self.spawn_request.theta = 0.0
            self.spawn_request.name = "body_turtle"
            self.spawn_turtle(self.spawn_request, self.draw_body_circle)
    def draw_body_circle(self, future):
        self.draw_circle("body_turtle", 2.0, self.stop_body_turtle)
    def stop_body_turtle(self):
        self.stop_turtle("body_turtle")
    def spawn_turtle(self, request, callback):
        future = self.spawn_client.call_async(request)
        future.add_done_callback(callback)
    def draw_circle(self, turtle_name, radius, callback):
        pub = self.create_publisher(Twist, f'/{turtle_name}/cmd_vel', 10)
        twist = Twist()
        circle_time = 10.0
        twist.linear.x = 2 * math.pi * radius / circle_time
        if turtle_name == "head_turtle":
            twist.angular.z = -2 * math.pi / circle_time 
        elif turtle_name == "body_turtle":
            twist.angular.z = 2 * math.pi / circle_time
        self.get_logger().info(f'Drawing circle with turtle {turtle_name} - radius: {radius}, linear speed: {twist.linear.x}, angular speed: {twist.angular.z}')
        def timer_callback():
            nonlocal pub, twist
            pub.publish(twist)
        def stop_turtle():
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            pub.publish(twist)
            callback()
            self.get_logger().info(f'{turtle_name} stopped')
        self.create_timer(circle_time, stop_turtle)
        self.create_timer(0.1, timer_callback)
    def stop_turtle(self, turtle_name):
        pub = self.create_publisher(Twist, f'/{turtle_name}/cmd_vel', 10)
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)
def main(args=None):
    rclpy.init(args=args)
    turtle_circle_drawer = TurtleCircleDrawer()
    rclpy.spin(turtle_circle_drawer)
    turtle_circle_drawer.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()