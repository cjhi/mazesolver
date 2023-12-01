#Node for getting Neato to move and follow correct path through maze

#Copied over from warmup project

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import time
from time import sleep

#For testing:
maze = {'A':(0,0),
        'B': (0.5, 0),
        'C': (1, 0),
        'D':(0,0.5),
        'E': (0.5, 0.5),
        'F': (1, 0.5),
        'G':(0,1),
        'H': (0.5, 1),
        'I': (1, 1),
        }

path = ['A', 'B', 'E', 'H', 'I']


#add path correction using odom?
class Follow_Path(Node):
    def __init__(self):
        super().__init__("follow_path")
        self.create_timer(0.1, self.run_loop)
        self.vel_pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.scan_sub = self.create_subscription(
            LaserScan,
            "scan",
            self.handle_scan,
            qos_profile=qos_profile_sensor_data,
        )

        self.maze = maze #for storing representation of maze as dictionary w/ node labels as keys, (x,y) as values
        self.path = path #for storing path (ordered list of node labels to visit)
        self.current_node = [] #for storing current node key
        self.target_node = [] #for storing target node key
        self.robot_orientation = 0
        self.unit_distance = 0.5 #distance between two side-by-side nodes

    def handle_scan(self, scan):
        pass

    def run_loop(self):
        pass
        msg = Twist()
        forward_time = 1.62 #amount of time to move forward 0.5m at 0.3m/s
        turn_time = 5.22 #amount of time to turn pi/2 rad at 0.3 rad/s? seems wrong
        #print("forward_time is: ", forward_time)

        #set start orientation:
        self.robot_orientation = 90
        print("starting maze")
        #assuming no diagonal movement
        for i in range (0,len(self.path)-1):
            current_pos = self.path[i]
            target_pos = self.path[i+1]
            #print("current index is: ", i)
            print("current location is: ", current_pos)
            x_displacement = maze[target_pos][0] - maze[current_pos][0] 
            y_displacement = maze[target_pos][1] - maze[current_pos][1] 

            #If we need to move vertically:
            if (x_displacement == 0) & (abs(y_displacement) == self.unit_distance):
                
                #check what orientation robot needs to be in
                if y_displacement<0:
                    target_orientation = -90 #face robot in correct y direction
                elif y_displacement >0:
                    target_orientation = 90
                
                #rotate to correct orientation
                if self.robot_orientation != target_orientation:
                    if target_orientation < self.robot_orientation:
                        #TODO: turn robot until facing correct orientation

                        while (self.robot_orientation != target_orientation):
                            print("turning right (real)")
                            msg.angular.z = -0.3
                            self.vel_pub.publish(msg)

                            #start timer
                            t = time.time()

                            #wait until turn_time seconds has elapsed
                            while((time.time() - t) < turn_time):
                                sleep(0.1)

                            #stop
                            msg.angular.z = 0.0
                            self.vel_pub.publish(msg)
                            sleep(1.0)

                            #TODO: update self.robot_orientation
                            self.robot_orientation = self.robot_orientation - 90
                            print("robot orientation is: ", self.robot_orientation)
                        
                    else:
                        #TODO: turn robot until facing correct orientation
                        while (self.robot_orientation != target_orientation):
                            print("turning left (real)")

                            msg.angular.z = 0.3
                            self.vel_pub.publish(msg)

                            #start timer
                            t = time.time()

                            #wait until turn_time seconds has elapsed
                            while((time.time() - t) < turn_time):
                                sleep(0.1)

                            #stop
                            msg.angular.z = 0.0
                            self.vel_pub.publish(msg)
                            sleep(1.0)
                            self.robot_orientation = self.robot_orientation + 90
                            print("robot orientation is: ", self.robot_orientation)
                
                #Move in correct direction
                #TODO: move forward unit_distance
                print("moving forward")
                msg.linear.x = 0.3
                self.vel_pub.publish(msg)

                #start timer
                t = time.time()

                #wait until 1.67 seconds has elapsed
                while((time.time() - t) < forward_time):
                    sleep(0.1)

                #stop
                msg.linear.x = 0.0
                self.vel_pub.publish(msg)
                sleep(1.0)

            #If we need to move horizontally:
            elif (y_displacement == 0) & (abs(x_displacement) == self.unit_distance):
                #check what orientation robot needs to be in
                if x_displacement<0:
                    target_orientation = -180 #face robot in correct y direction
                elif x_displacement >0:
                    target_orientation = 0
                
                #rotate to correct orientation
                if self.robot_orientation != target_orientation:
                    if target_orientation < self.robot_orientation:
                        #TODO: turn robot until facing correct orientation

                        while (self.robot_orientation != target_orientation):
                            print("turning right (real)")
                            msg.angular.z = -0.3
                            self.vel_pub.publish(msg)

                            #start timer
                            t = time.time()

                            #wait until turn_time seconds has elapsed
                            while((time.time() - t) < turn_time):
                                sleep(0.1)

                            #stop
                            msg.angular.z = 0.0
                            self.vel_pub.publish(msg)
                            sleep(1.0)
                            self.robot_orientation = self.robot_orientation - 90
                            print("robot orientation is: ", self.robot_orientation)
                    else:
                        #TODO: turn robot until facing correct orientation
                        while (self.robot_orientation != target_orientation):
                            print("turning left (real)")

                            msg.angular.z = 0.3
                            self.vel_pub.publish(msg)

                            #start timer
                            t = time.time()

                            #wait until turn_time seconds has elapsed
                            while((time.time() - t) < turn_time):
                                sleep(0.1)

                            #stop
                            msg.angular.z = 0.0
                            self.vel_pub.publish(msg)
                            sleep(1.0)
                            self.robot_orientation = self.robot_orientation + 90
                            print("robot orientation is: ", self.robot_orientation)
                    
                #Move in correct direction
                #TODO: move forward unit_distance
                print("moving forward")
                msg.linear.x = 0.3
                self.vel_pub.publish(msg)

                #start timer
                t = time.time()

                #wait until 1.67 seconds has elapsed
                while((time.time() - t) < forward_time):
                    sleep(0.1)

                #stop
                msg.linear.x = 0.0
                self.vel_pub.publish(msg)
                sleep(1.0)

        print("finished maze")



def main(args=None):
    rclpy.init(args=args)
    node = Follow_Path()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
