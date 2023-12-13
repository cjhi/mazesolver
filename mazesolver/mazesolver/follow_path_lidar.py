# Node for getting Neato to move and follow correct path through maze

# Note: this file assumes the maze given has orthogonal walls only with uniform spacing of 1 meter
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
#from nav_msgs.msg import Odometry
import math
import time
from time import sleep
from numpy import inf

# Solution path for large_example.txt as solved in dijkstra.py
new_path = [(0, 4), (1, 4), (1, 5), (1, 6), (1, 7), (2, 7), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (7, 7), (8, 7), (8, 6), (7, 6), (6, 6), (6, 5), (6, 4), (7, 4), (7, 3), (8, 3), (8, 2), (9, 2), (9, 1), (10, 1), (10, 2), (10, 3), (10, 4), (9, 4), (9, 5), (9, 6), (10, 6), (10, 5), (11, 5)]

#These values to be tuned:
forward_time = 1.62*2 #amount of time to move forward 1.0m at 0.3m/s
turn_time = 5.22 #amount of time to turn pi/2 rad at 0.3 rad/s

#set start robot orientation:
start_orientation = 90

class Follow_Path_Lidar(Node):
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

        self.path = new_path #for storing solution maze path (ordered list of node labels to visit)
        self.robot_orientation = start_orientation #for storing current robot orientation
        self.target_orientation = 0 #for storing next target orientation of robot

        #self.odom_frame = "odom"        # the name of the odometry coordinate frame - unused

        #for storing lidar scan data
        self.backLeftScan = []
        self.backRightScan= []
        self.forwardLeftScan = []
        self.forwardRightScan = []
        self.straightForward = []
        self.straightBackward = []
        self.left = inf
        self.right = inf

        #for counting position in path
        self.i = 0

        #temp variables for handle_scan()
        self.turn_back_left = False
        self.turn_back_right = False

        print("starting maze")

    #Main function - takes in scan and then runs the Neato through the maze
    def handle_scan(self, scan):
        #self.scan = scan #if we wanted to continously update the scan and access it from another function, would use this
        
        #Run through maze
        if self.i < (len(self.path)-1): #check if we've finished the maze
            #Access lidar scan and separate into four quadrants
            #Note: for physical neatos, remove zeroes to prevent issues with min() later on (can take code from obstacle_avoidance)
            self.backLeftScan = list(scan.ranges[91:179])
            self.backRightScan= list(scan.ranges[181:269])
            self.forwardLeftScan = list(scan.ranges[1:89])
            self.forwardRightScan = list(scan.ranges[271:359])

            #Look at scan distance straight ahead, straight back, to left, and to right
            self.straightForward = scan.ranges[0]
            self.straightBackward = scan.ranges[180]
            self.left = scan.ranges[90]
            self.right = scan.ranges[270]

            #Access current position and target position, calculate necessary x and y movement distance
            current_pos = self.path[self.i]
            target_pos = self.path[self.i+1]
            x_displacement = target_pos[0] - current_pos[0] 
            y_displacement = target_pos[1] - current_pos[1]

            correctStraight = 0.7 #seconds to move forward or back when correcting
            correctTurn = 0.65 #seconds to turn for while turning

            # Do path correction:
            #If too close to wall up ahead, back up
            if (self.straightForward < 0.42):
                    #Back up
                    msg = Twist()
                    msg.linear.x = -0.3
                    sleep(correctStraight)
                    self.vel_pub.publish(msg)

                    #Stop
                    msg = Twist()
                    msg.linear.x = 0.0
                    self.vel_pub.publish(msg)
                    sleep(0.4)

            #If too close to wall directly behind, move forward
            if (self.straightBackward < 0.3):
                    #Move forward
                    msg = Twist()
                    msg.linear.x = 0.3
                    self.vel_pub.publish(msg)
                    sleep(correctStraight)

                    #Stop
                    msg = Twist()
                    msg.linear.x = 0.0
                    self.vel_pub.publish(msg)
                    sleep(0.4)
            
            #If too far from wall up ahead, move forward
            if (self.straightForward > 0.7 and self.straightForward <1.1):
                #Move Forward
                msg = Twist()
                msg.linear.x = 0.3
                self.vel_pub.publish(msg)
                sleep(correctStraight)

                #Stop
                msg = Twist()
                msg.linear.x = 0.0
                self.vel_pub.publish(msg)

            #If too close to wall on left or right, turn slightly away from it before moving forward
            if (self.left < 0.4 or self.right <0.4):
                self.turn_back = True #After the next move(), the Neato will turn back before making next movement when this is toggled

                #Check if wall is too close
                if self.left<0.5:   #if wall on left is too close, turn right
                    msg = Twist()
                    msg.angular.z = -0.3
                    self.turn_back_left = True
                else:               #if wall on right is too close, turn left
                    msg = Twist()
                    msg.angular.z = 0.3
                    self.turn_back_right = True
                
                #Send commands to Neato
                self.vel_pub.publish(msg)
                sleep(correctTurn)

                #Stop
                msg = Twist()
                msg.angular.z = 0.0
                self.vel_pub.publish(msg)


            #Check x-y direction the Neato needs to go in:
            if (x_displacement == 0) & (abs(y_displacement) > 0):     
                #check what orientation robot needs to be in
                if y_displacement<0:
                    self.target_orientation = -90 #face robot in correct x direction
                elif y_displacement >0:
                    self.target_orientation = 90
            elif (y_displacement == 0) & (abs(x_displacement) > 0):
                #check what orientation robot needs to be in
                if x_displacement<0:
                    self.target_orientation = -180 #face robot in correct y direction
                elif x_displacement >0:
                        self.target_orientation = 0


            #If we need to turn, turn
            if(self.target_orientation != self.robot_orientation):
                self.turn() 
            else:   #Otherwise, move forward
                self.move()
                self.i = self.i + 1 #incremement
        
            #If we previously corrected by turning away from a wall, turn back to original orientation
            if (self.turn_back_right):
                msg = Twist()
                msg.angular.z = -0.3
                self.turn_back_right = False  
                self.vel_pub.publish(msg)
                sleep(correctTurn)
            if (self.turn_back_left):
                msg = Twist()
                msg.angular.z = 0.3
                self.turn_back_left = False  
                self.vel_pub.publish(msg)
                sleep(correctTurn)

    #Function for turning Neato to correct orientation
    def turn(self):
        msg = Twist()

        #Check if we need to turn
        if self.robot_orientation != self.target_orientation:
            
            #Turn right, if needed:
            if self.target_orientation < self.robot_orientation:
                
                #Turn robot until facing correct orientation
                while (self.robot_orientation != self.target_orientation):
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

                    #update self.robot_orientation to current orientation
                    self.robot_orientation = self.robot_orientation - 90
                            
            #Or turn left:
            else:
                #Turn robot until facing correct orientation
                while (self.robot_orientation != self.target_orientation):
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

                    #updat self.robot_orientation to current orientation
                    self.robot_orientation = self.robot_orientation + 90

    #Function for moving forward one unit distance
    def move(self):
        msg = Twist()

        #Move forward unit distance
        msg.linear.x = 0.3
        self.vel_pub.publish(msg)

        #start timer
        t = time.time()

        #wait until forward_time seconds has elapsed
        while((time.time() - t) < forward_time):
            sleep(0.1)

        #stop
        msg.linear.x = 0.0
        self.vel_pub.publish(msg)
        sleep(1.0)

    def run_loop(self):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = Follow_Path_Lidar()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
