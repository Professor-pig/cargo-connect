#!/usr/bin/env pybricks-micropython

# from pybricks.hubs import EV3Brick
import pybricks.hubs as hub

# from pybricks.ev3devices import Motor, ColorSensor, InfraredSensor, GyroSensor
import pybricks.ev3devices as devices

# from pybricks.parameters import Port, Stop, Direction, Button, Color ,  [oiufeds43Q`  `YRESA`]
import pybricks.parameters as parameters

# from pybricks.tools import wait, StopWatch, DataLog

# from pybricks.robotics import DriveBase

# from pybricks.media.ev3dev import SoundFile, ImageFile
import time
from robot import Robot
import threading

robot = Robot()
from_home = True

def route_3():
    def func_1():
        time.sleep(0.8)
        robot.A.spin_for_deg(500)
    
    def func_2():
        robot.advance(10)

    if from_home:
        thread_1 = threading.Thread(target=func_1)
        robot.A.spin_for_deg(-1300)
        robot.advance_without_acceleration(60, 500, 0.79)
        time.sleep(0.5)
        robot.A.spin_for_deg(1200)
        robot.advance_without_acceleration(25, 500, 0.9)
        robot.A.spin_for_deg(-500)
        thread_1.start()
        robot.advance(40, 600, 0.9)
    
    thread_2 = threading.Thread(target=func_2)
    robot.retreat(4)
    robot.A.spin_for_deg(-600)
    robot.turn(-65)
    thread_2.start()
    robot.A.spin_for_deg(1790)
    robot.advance(27)
    robot.D.spin_for_deg(-100)
    robot.turn(34)
    robot.advance(28)

def put_down_left_arm():
    robot.A.spin_for_deg(-500)

def put_half_down_left_arm():
    robot.A.spin_for_deg(-300)

def raise_up_left_arm():
    robot.A.spin_for_deg(500)

def raise_half_up_left_arm():
    robot.A.spin_for_deg(300)

def put_down_folk():
    robot.D.spin_for_deg(300)
    
def route_1():
    # robot.advance(75, 300, 0.979)
    # time.sleep(0.1)
    # robot.turn(50)
    robot.advance(91, 300, 0.979)
    time.sleep(0.1)
    robot.turn(35)
    
    threading.Thread(target=put_half_down_left_arm).start()
    # threading.Thread(target=put_down_folk).start()
    #push
    robot.advance(47, 300, 0.979)
    #raise up arm
    raise_half_up_left_arm()
    
    robot.advance(34, 300, 0.979)
    time.sleep(0.1)
    robot.turn(90)
    time.sleep(0.1)
    put_down_folk()
    robot.advance(16, 300, 0.979)
    robot.advance(19, 100, 0.979)
    
    put_down_left_arm()
    


    


robot.brick.speaker.set_volume(5)
robot.brick.speaker.beep(440, 200)
route_1()

robot.brick.speaker.beep(440, 200)
