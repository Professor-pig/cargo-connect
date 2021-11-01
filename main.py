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



def arm_goes_back_with_pushing_west_bridge():
    time.sleep(0.8)
    robot.left_motor.spin_for_deg(500)


def func_2():
    robot.advance(10)


def route_3():
    print("route 3")
    route_3_stage_1 = True
    route_3_stage_2 = False 
    route_3_go_home = False # go home
    if route_3_stage_1:
        arm_goes_back_with_pushing_west_bridge_thread = threading.Thread(target=arm_goes_back_with_pushing_west_bridge)
        robot.left_motor.spin_for_deg(-1200) # push truck out home

        robot.advance_without_acceleration(63, 500, 0.79)
        time.sleep(0.5)
        robot.left_motor.spin_for_deg(2100)
        robot.left_motor.spin_for_deg(-1100)
        robot.advance_without_acceleration(22, 500, 0.9) 
        robot.left_motor.spin_for_deg(-200) # arm goes out, preparing to push west bridge
        threading.Thread(target=arm_goes_back_with_pushing_west_bridge).start()
        robot.advance(37, 600, 0.9) # keep going and pushing west bridge

    if route_3_stage_2:
        thread_2 = threading.Thread(target=func_2)
        # robot.retreat(4) do not need retreat
        robot.left_motor.spin_for_deg(-600)
        robot.turn(-65)
        thread_2.start()
        robot.left_motor.spin_for_deg(2000)
        robot.advance(27)
        robot.right_motor.spin_for_deg(-100)
        robot.turn(32)
        robot.advance(28)
    
    if route_3_go_home:
        pass

def lower_left_motor():
    robot.left_motor.spin_for_deg(-550)

def put_half_down_left_motor():
    robot.left_motor.spin_for_deg(-300)

def raise_left_motor():
    robot.left_motor.spin_for_deg(555)

def raise_half_up_left_motor():
    robot.left_motor.spin_for_deg(300)

def put_down_fork():
    robot.right_motor.spin_for_deg(300)

def lift_fork():
    robot.right_motor.spin_for_deg(-305)

def push_helicopter():
    robot.retreat(74, 300)
    robot.turn(51)
    robot.retreat(16, 300)
    robot.advance(16, 300)
    robot.turn(-51)

def push_train():
    lower_left_motor()
    robot.advance(74)
    raise_left_motor()

def route_1_go_home_with_pushing_helicopter():
    # push helicopter
    robot.retreat(33, 300)
    robot.turn(51)
    robot.retreat(16, 300)

    # return home
    robot.advance(34, 300)
    robot.turn(40)
    robot.advance(73, 300)
    robot.turn(-31)
    robot.advance(24, 300)
    robot.turn(47)
    robot.advance_without_acceleration(70, 1000)

def route_1():
    print("route1")
    robot.advance(84, 300, 0.979)
    time.sleep(0.1)
    robot.turn(33)
    
    # threading.Thread(target=lower_left_motor).start()

    do_not_push = True
    if do_not_push:    
        robot.advance(85, 300, 0.98)
    else:
        robot.advance(34, 300, 0.979)
        #push
        lower_left_motor()
        robot.advance_without_acceleration(14, 400, 0.7)
    
        #raise up arm
        raise_left_motor()
    
        robot.advance(30, 300, 0.979)
    
    time.sleep(0.1)
    robot.turn(89)
    time.sleep(0.1)
    put_down_fork()
    robot.advance(26, 300, 0.979)
    lift_fork()
    lower_left_motor()
    raise_left_motor()
    
    robot.retreat(41, 300)

    # push train
    lower_left_motor()
    robot.advance(41, 300)
    raise_left_motor()

    route_1_go_home_with_pushing_helicopter()

def route_4():
    # robot.advance(73, 300, 0.979)
    # time.sleep(0.1)
    robot.pivot(30, 300)

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

def push_green_and_flip_engine():
    robot.advance(24)
    robot.retreat(15)

def pull_small_plane():
    robot.right_motor.spin_for_deg(1800)

def pull_big_plane():
    robot.left_motor.spin_for_deg(-600)
    time.sleep(0.5)

def release_grey_cargo():
    robot.left_motor.spin_for_deg(600)

def route_2():
    # print("route 2")
    # robot.advance(67, 300)
    # time.sleep(0.1)
    # robot.turn(40)
    # time.sleep(0.1)
    # push_green_and_flip_engine()
    pull_small_plane()
    # pull_big_plane()
    # robot.retreat(8)
    # release_grey_cargo()
    # robot.retreat(45)


robot.brick.speaker.set_volume(5)
debug = False
if debug:
    robot.left_motor.spin_for_deg(-1200) # push truck out home
    time.sleep(1)
    robot.left_motor.spin_for_deg(2100)
    robot.left_motor.spin_for_deg(-900)
else:    
    robot.brick.speaker.beep(440, 200)
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
