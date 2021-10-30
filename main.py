#!/usr/bin/env pybricks-micropython

# from pybricks.hubs import EV3Brick
import pybricks.hubs as hub

# from pybricks.ev3devices import Motor, ColorSensor, InfraredSensor, GyroSensor
import pybricks.ev3devices as devices

# from pybricks.parameters import Port, Stop, Direction, Button, Color
import pybricks.parameters as parameters

# from pybricks.tools import wait, StopWatch, DataLog

# from pybricks.robotics import DriveBase

# from pybricks.media.ev3dev import SoundFile, ImageFile
import time
from robot import Robot
import threading

robot = Robot()
from_home = True


def func_1():
    time.sleep(0.8)
    robot.left_arm.spin_for_deg(500)


def func_2():
    robot.advance(10)


def route_3():
    stop_at_chichen = False
    if from_home:
        thread_1 = threading.Thread(target=func_1)
        robot.left_arm.spin_for_deg(-1300)
        robot.advance_without_acceleration(60, 500, 0.75)
        time.sleep(0.5)
        robot.left_arm.spin_for_deg(1200)

        if not stop_at_chichen:
            robot.advance_without_acceleration(25, 500, 0.9)
            robot.left_arm.spin_for_deg(-500)
            thread_1.start()
            robot.advance(36, 600, 0.9)

    if not stop_at_chichen:    
        thread_2 = threading.Thread(target=func_2)
        # robot.retreat(4) do not need retreat
        robot.left_arm.spin_for_deg(-600)
        robot.turn(-65)
        thread_2.start()
        robot.left_arm.spin_for_deg(2000)
        robot.advance(27)
        robot.right_arm.spin_for_deg(-100)
        robot.turn(32)
        # robot.advance(28)

def put_down_left_arm():
    robot.left_arm.spin_for_deg(-550)

def put_half_down_left_arm():
    robot.left_arm.spin_for_deg(-300)

def raise_left_arm():
    robot.left_arm.spin_for_deg(555)

def raise_half_up_left_arm():
    robot.left_arm.spin_for_deg(300)

def put_down_fork():
    robot.right_arm.spin_for_deg(300)

def lift_fork():
    robot.right_arm.spin_for_deg(-305)

def route_1_go_home_with_pushing_helicopter():
    robot.retreat(33, 300)
    robot.turn(51)
    robot.retreat(16, 300)
    robot.advance(34, 300)
    robot.turn(40)
    robot.advance(73, 300)
    robot.turn(-31)
    robot.advance(24, 300)
    robot.turn(47)
    robot.advance(70)

def route_1():
    print("route1")
    robot.advance(84, 300, 0.979)
    time.sleep(0.1)
    robot.turn(33)
    
    # threading.Thread(target=put_down_left_arm).start()

    do_not_push = True
    if do_not_push:    
        robot.advance(85, 300, 0.98)
    else:
        robot.advance(34, 300, 0.979)
        #push
        put_down_left_arm()
        robot.advance_without_acceleration(14, 400, 0.7)
    
        #raise up arm
        raise_left_arm()
    
        robot.advance(30, 300, 0.979)
    
    time.sleep(0.1)
    robot.turn(89)
    time.sleep(0.1)
    put_down_fork()
    robot.advance(26, 300, 0.979)
    lift_fork()
    put_down_left_arm()
    raise_left_arm()
    
    robot.retreat(41, 300)

    # push train
    put_down_left_arm()
    robot.advance(41, 300)
    raise_left_arm()

    route_1_go_home_with_pushing_helicopter()

def route_4():
    # robot.advance(73, 300, 0.979)
    # time.sleep(0.1)
    robot.pivot(30, 300)

def route_2():
    print("route2")


def test_route_1():
    def test_route_1_turn():
        angle_offset = 2
        for _ in range(4):
            # robot.pivot(90)
            # robot.turn(-90 + angle_offset, 100)
            robot.turn(90 - angle_offset, 100)
            time.sleep(0.5)

    def test_route_1_advance():
        robot.advance(100, 300, 0.965)

    test_route_1_advance()

def route_2():
    print("route 2")
    robot.advance(68, 300)
    time.sleep(0.1)
    robot.turn(39)
    time.sleep(0.1)
    robot.advance(24, 300)
    robot.retreat(19, 300)
    robot.right_arm.spin_for_deg(650)
    # time.sleep(0.1)
    robot.turn(-45)
    # time.sleep(0.1)
    robot.right_arm.spin_for_deg(-650)


robot.brick.speaker.set_volume(5)
robot.brick.speaker.beep(440, 200)
debug = False
if debug:
    route_1_go_home_with_pushing_helicopter()
else:    
    attachment_color = robot.colour_middle.color()
    print(attachment_color)
    if attachment_color == parameters.Color.YELLOW:
        route_4()
    elif attachment_color == parameters.Color.RED:
        route_1()
    elif attachment_color == parameters.Color.BLUE:
        route_3()
    elif attachment_color == parameters.Color.BLACK:
        route_2()

robot.brick.speaker.beep(440, 200)
