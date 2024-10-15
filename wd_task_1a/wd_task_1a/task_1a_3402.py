
# import rclpy
# from rclpy.node import Node
# from turtlesim.srv import SetPen, TeleportAbsolute
# from geometry_msgs.msg import Twist
from math import pi,sqrt,atan2

# class TurtleSimTester(Node):

#     def __init__(self):
#         super().__init__('turtle_sim_tester')

#         # Publisher for cmd_vel
#         self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

#         # Service clients for pen and teleport
#         self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
#         self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')

#         # Wait for services to be available
#         self.pen_client.wait_for_service()
#         self.teleport_client.wait_for_service()

    # def set_pen(self, r, g, b, width, off):
    #     request = SetPen.Request()
    #     request.r = r
    #     request.g = g
    #     request.b = b
    #     request.width = width
    #     request.off = off
    #     future = self.pen_client.call_async(request)
    #     rclpy.spin_until_future_complete(self, future)
    #     if future.result():
    #         self.get_logger().info(f"Pen set to color: ({r}, {g}, {b}), width: {width}, off: {off}")
    #     else:
    #         self.get_logger().error("Pen service failed.")

    # def teleport(self, x, y, theta):
    #     request = TeleportAbsolute.Request()
    #     request.x = x
    #     request.y = y
    #     request.theta = theta
    #     future = self.teleport_client.call_async(request)
    #     rclpy.spin_until_future_complete(self, future)
    #     if future.result():
    #         self.get_logger().info(f"Turtle teleported to: ({x}, {y}) with angle {theta} radians.")
    #     else:
    #         self.get_logger().error("Teleport service failed.")

#     def move_circle(self, linear, angular, duration):
#         vel_msg = Twist()
#         vel_msg.linear.x = linear
#         vel_msg.angular.z = angular
#         self.cmd_pub.publish(vel_msg)
#         self.get_logger().info(f"Turtle moving in circle: linear={linear}, angular={angular} for {duration} seconds")
#         self.get_clock().sleep_for(rclpy.duration.Duration(seconds=duration))
#         self.cmd_pub.publish(Twist())  # Stop the turtle

#     def move_line(self, linear_x, duration):
#         vel_msg = Twist()
#         vel_msg.linear.x = linear_x
#         self.cmd_pub.publish(vel_msg)
#         self.get_logger().info(f"Turtle moving straight with velocity={linear_x} for {duration} seconds")
#         self.get_clock().sleep_for(rclpy.duration.Duration(seconds=duration))
#         self.cmd_pub.publish(Twist())  # Stop the turtle


# def main(args=None):
#     rclpy.init(args=args)
#     node = TurtleSimTester()

#     print("TurtleSim Test Options:")
#     print("1. Test Teleport Service")
#     print("2. Test SetPen Service")
#     print("3. Test Movement (Circle or Line)")

#     user_choice = input("Enter the number of the test you want to run: ")

#     if user_choice == "1":
#         x = float(input("Enter x-coordinate to teleport: "))
#         y = float(input("Enter y-coordinate to teleport: "))
#         theta = float(input("Enter angle (theta in radians): "))
#         node.teleport(x, y, theta)

#     elif user_choice == "2":
#         r = int(input("Enter red value (0-255): "))
#         g = int(input("Enter green value (0-255): "))
#         b = int(input("Enter blue value (0-255): "))
#         width = int(input("Enter pen width: "))
#         off = int(input("Enter 1 to turn off the pen, 0 to keep it on: "))
#         node.set_pen(r, g, b, width, off)

#     elif user_choice == "3":
#         move_choice = input("Move in a circle or line? (Enter 'circle' or 'line'): ").lower()
#         if move_choice == 'circle':
#             linear = float(input("Enter linear velocity: "))
#             angular = float(input("Enter angular velocity: "))
#             duration = float(input("Enter duration in seconds: "))
#             node.move_circle(linear, angular, duration)
#         elif move_choice == 'line':
#             linear_x = float(input("Enter linear velocity: "))
#             duration = float(input("Enter duration in seconds: "))
#             node.move_line(linear_x, duration)
#         else:
#             print("Invalid choice.")
    
#     else:
#         print("Invalid test option selected.")

#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()

import rclpy
from rclpy.node import Node
from rclpy.exceptions import ParameterNotDeclaredException
from turtlesim.srv import SetPen, TeleportAbsolute
from geometry_msgs.msg import Twist
from math import atan2

class TurtleSimCommander(Node):

    def __init__(self):
        super().__init__("Turtle_Sim_Commander")

        #Publisher Node
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info("Created cmd_vel publisher")
        
        #Service clients
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        self.get_logger().info("Created pen service client")
        self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.get_logger().info("Created teleport service client")
        self.clear_client = self.create_client(SetPen, '/clear')
        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Pen service not available, waiting again...")
        while not self.teleport_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Teleport service not available, waiting again...")
        # while not self.clear_client.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info("Clear service not available, waiting again...")
        self.pen_client.wait_for_service()
        self.get_logger().info("Pen service available")
        self.teleport_client.wait_for_service()
        self.get_logger().info("Teleport service available")
        # self.clear_client.wait_for_service()
        # self.get_logger().info("Clear Services available")



    def move_circle(self, linear, angular, duration):
        vel_msg = Twist()
        vel_msg.linear.y = linear
        vel_msg.angular.z = angular
        self.pub.publish(vel_msg)
        self.get_logger().info(f"Turtle moving in circle: linear.y={linear}, angular={angular} for {duration} seconds")
        self.get_clock().sleep_for(rclpy.duration.Duration(seconds=duration))
        self.pub.publish(Twist())  # Stop the turtle

    def move_line(self, linear_x, linear_y, duration):
        vel_msg = Twist()
        vel_msg.linear.x = linear_x
        # vel_msg.linear.y = linear_y
        self.pub.publish(vel_msg)
        self.get_logger().info(f"Turtle moving straight with velocity={linear_x}i + {linear_y}j for {duration} seconds")
        self.get_clock().sleep_for(rclpy.duration.Duration(seconds=duration))
        self.pub.publish(Twist())  # Stop the turtle
        self.pub.publish(Twist())  # Stop the turtle
        self.pub.publish(Twist())  # Stop the turtle

    

    # def set_pen(self, r, g, b, width, off):
    #     self.get_logger().info("Setting pen")
    #     request = SetPen.Request()
    #     request.r = r
    #     request.g = g
    #     request.b = b
    #     request.width = width
    #     request.off = off

    #     # Call the service synchronously
    #     self.get_logger().info("Calling pen service")
    #     response = self.pen_client.call(request)

    #     # Check if the service call was successful
    #     while not response:
    #         self.get_logger().error("Pen service failed.")
    #         self.get_logger().info("Trying again...")
    #         response = self.pen_client.call(request)
    #     else:
    #         self.get_logger().info(f"Pen set to color: ({r}, {g}, {b}), width: {width}, off: {off}")

    def teleport(self, x, y, theta, pen_off=False, timeout_sec=2.0):
        self.get_logger().info("Teleporting")
        
        if pen_off:
            self.set_pen(255, 255, 255, 2, 1)
        
        request = TeleportAbsolute.Request()
        request.x = x
        request.y = y
        request.theta = float(theta)

        # Call the service asynchronously
        future = self.teleport_client.call_async(request)

        # Wait for the result, with a timeout
        rclpy.spin_until_future_complete(self, future, timeout_sec=timeout_sec)

        # Check if the service call was successful
        if future.result() is not None:
            self.get_logger().info(f"Turtle teleported to: ({x}, {y}) with angle {theta} radians.")
            if pen_off:
                self.set_pen(255, 255, 255, 2, 0)
        else:
            self.get_logger().error("Teleport service failed or timed out.")


# import rclpy
# from turtlesim.srv import SetPen

    def set_pen(self, r, g, b, width, off, timeout_sec=2.0):
        self.get_logger().info("Setting pen")
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        # Call the service asynchronously
        future = self.pen_client.call_async(request)

        # Wait for the result, with a timeout
        rclpy.spin_until_future_complete(self, future, timeout_sec=timeout_sec)

        if future.result() is not None:
            self.get_logger().info(f"Pen set to color: ({r}, {g}, {b}), width: {width}, off: {off}")
        else:
            self.get_logger().error("Pen service failed or timed out.")


    def draw_circle(self, center_x, center_y, diameter):

        print("Drawing circle at: ", center_x, center_y, diameter)
        self.teleport(center_x + diameter/2, center_y, 0.0, True)
        print("Teleported")
        self.set_pen(255, 255, 255, 2, 0)
        self.move_circle(10.0*diameter/2, 10.0, pi/5.0)
        print("Circle drawn")

    def draw_line(self, x_start, y_start, x_end, y_end):

        print("Drawing line from: ", x_start, y_start, " to ", x_end, y_end)
        # self.teleport(x_start, y_start, 0, True)
        # self.set_pen(255, 255, 255, 2, 0)
        dx = x_end - x_start
        dy = y_end - y_start
        distance = sqrt(dx**2 + dy**2)
        angle = atan2(dy, dx)
        self.teleport(x_start, y_start, angle, True)
        self.move_line((distance)*1.0, 0.0, 1.0)
        print("Line drawn")


    # def execute(self):
        
    #     print("Executing") 
    #     # Draw the four circles (propellers)
    #     self.draw_circle(2.0, 2.0, 2.0)
    #     self.draw_circle(2.0, 8.0, 2.0)
    #     self.draw_circle(8.0, 8.0, 2.0)
    #     self.draw_circle(8.0, 2.0, 2.0)

    #     # Draw the square frame lines
    #     self.draw_line(3.0, 5.0, 5.0, 3.0)
    #     self.draw_line(3.0, 5.0, 7.0, 5.0)
    #     self.draw_line(7.0, 5.0, 7.0, 3.0)
    #     self.draw_line(7.0, 3.0, 3.0, 5.0)

    #     # Draw the lines connecting the circles to the square
    #     self.draw_line(2.0, 2.0, 4.0, 4.0)
    #     self.draw_line(2.0, 8.0, 4.0, 6.0)
    #     self.draw_line(8.0, 8.0, 6.0, 6.0)  
    #     self.draw_line(8.0, 2.0, 6.0, 4.0)

    #     # Teleport the turtle to the center of the drawing
    #     self.teleport(5.0, 5.0, 0.0, True)  

    #     self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    print("Initializing")
    node = TurtleSimCommander()
    print("Initialized")
    circles = [[2.0, 2.0, 2.0], [2.0, 8.0, 2.0], [8.0, 8.0, 2.0], [8.0, 2.0, 2.0]]
    lines = [[3.0, 5.0, 5.0, 3.0], [5.0, 3.0, 7.0, 5.0], [7.0, 5.0, 5.0, 7.0], [5.0, 7.0, 3.0, 5.0],[2.0, 2.0, 4.0, 4.0], [2.0, 8.0, 4.0, 6.0], [8.0, 8.0, 6.0, 6.0], [8.0, 2.0, 6.0, 4.0]]
    try:
        # rclpy.spin(node)
        node.get_logger().info("Executing")
        node.set_pen(255, 255, 255, 2, 1)
        node.get_logger().info("Pen set")
        # node.clear_client.call_async(SetPen.Request())
        # node.get_logger().info("Cleared")

        for circle in circles:
            node.draw_circle(circle[0], circle[1], circle[2])
            node.get_logger().info(f"Cirlce drawn at: {circle[0]}, {circle[1]} with diameter: {circle[2]}")
        for line in lines:
            node.draw_line(line[0], line[1], line[2], line[3])
            node.get_logger().info(f"Line drawn from: {line[0]}, {line[1]} to {line[2]}, {line[3]}")
        
        node.set_pen(255, 255, 255, 2, 1)
        node.teleport(5.0, 5.0, 0.0)
        node.get_logger().info("Teleported to center")
        
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()
