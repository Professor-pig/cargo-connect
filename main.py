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


def arm_goes_out_to_parepare_to_push_west_bridge():
    robot.left_motor.spin_for_deg(-200)

def arm_goes_back_with_pushing_west_bridge():
    time.sleep(0.8)
    robot.left_motor.spin_for_deg(600)


def go_to_cargo_connect_circle():
    robot.advance(10)
    print("fun_2 end")

def release_hinged():
    time.sleep(0.3)
    robot.left_motor.spin_for_deg(1100)

def raise_front_gate():
    robot.right_motor.spin_for_deg(-300)

def close_front_gate():
    robot.right_motor.spin_for_deg(300)

def route_3():
    print("route 3")
    route_3_stage_1 = True
    route_3_stage_2 = True
    route_3_go_home = False # go home
    push_east_bridge = False
    if route_3_stage_1:
        robot.left_motor.spin_for_deg(-1200) # push truck out home

        robot.advance_without_acceleration(63, 500, 0.79)
        time.sleep(0.5)
        robot.left_motor.spin_for_deg(2100)
        robot.left_motor.spin_for_deg(-1100)
        robot.advance_without_acceleration(22, 500, 0.9) 
        robot.left_motor.spin_for_deg(-200) # arm goes out, preparing to push west bridge
        # threading.Thread(target=arm_goes_out_to_parepare_to_push_west_bridge).start()
        threading.Thread(target=arm_goes_back_with_pushing_west_bridge).start()
        robot.advance(42.5, 500, 0.9) # keep going and pushing west bridge

    if route_3_stage_2:
        time.sleep(0.1)
        robot.retreat(6) # retreat to prepare to turn
        time.sleep(0.1)
        if push_east_bridge:
            robot.left_motor.spin_for_deg(-700)
            robot.turn(-65)
            threading.Thread(target=go_to_cargo_connect_circle).start()
            robot.left_motor.spin_for_deg(1700)
            robot.advance(53, 300, 0.979)
        else:
            robot.turn(-60)
            threading.Thread(target=release_hinged).start()
            robot.advance(64, 300, 0.979)
        raise_front_gate()
        time.sleep(0.1)
        robot.retreat(7, 300)
        time.sleep(0.1)
        robot.turn(30)
        time.sleep(0.1)
        close_front_gate()
        robot.advance(13)
    
        if route_3_go_home:
            robot.retreat_without_acceleration(40)
            robot.turn(15)
            robot.retreat_without_acceleration(80)
        else:
            robot.retreat(10)

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

# def route_1_go_home_with_pushing_helicopter():
#     # push helicopter
#     robot.retreat(33, 300)
#     robot.turn(51)
#     robot.retreat(16, 300)

#     # return home
#     robot.advance(34, 300)
#     robot.turn(40)
#     robot.advance(73, 300)
#     robot.turn(-30)
#     robot.advance(24, 300)
#     robot.turn(42)
#     robot.advance_without_acceleration(63, 500)

def route_1():
    print("route1")
    robot.advance(84, 300, 0.979)
    time.sleep(0.1)
    robot.turn(33)
    
    robot.advance(85, 400, 0.98)
    time.sleep(0.1)
    robot.turn(89)

    put_down_fork()
    robot.advance(27, 400, 0.979)
    lower_left_motor()
    
    threading.Thread(target=lift_fork).start()
    threading.Thread(target=raise_left_motor).start()
    robot.retreat(41, 300)

    # push train
    lower_left_motor()
    robot.advance(43, 300)    
    time.sleep(0.1)

    #go home
    threading.Thread(target=raise_left_motor).start()
    robot.retreat(19)
    time.sleep(0.1)
    robot.turn(87)
    robot.advance(86, 500, 0.98)
    robot.turn(-29)
    robot.advance(25, 300)
    robot.turn(34)
    robot.advance_without_acceleration(65, 1000)

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

def push_green_and_switch_engine():
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
    print("route 2")
    robot.advance(67, 300)
    time.sleep(0.1)
    robot.turn(40)
    time.sleep(0.1)
    push_green_and_switch_engine()
    pull_small_plane()
    pull_big_plane()
    robot.retreat(8)
    release_grey_cargo()
    robot.retreat(45)


robot.brick.speaker.set_volume(5)
debug = False
if debug:
    robot.retreat(10)
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
