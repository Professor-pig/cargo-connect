#!/usr/bin/env pybricks-micropython
import pybricks.hubs as hub
import pybricks.ev3devices as devices
import pybricks.parameters as parameters

import time
from robot import Robot
import threading

robot = Robot()


def withdraw_arm_from_bridge():
    time.sleep(2)
    robot.left_motor.spin_for_deg(650)

def go_to_cargo_connect_circle():
    robot.advance(10)

def release_hinged():
    time.sleep(0.7)
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
    if route_3_stage_1:
        robot.left_motor.spin_for_deg(-1300) # push truck out home

        robot.advance_without_acceleration(60, 600, 0.79)
        time.sleep(0.5)
        robot.left_motor.spin_for_deg(2200)
        robot.advance_without_acceleration(4.5, 500, 0.9) 
        robot.left_motor.spin_for_deg(-1350)
        threading.Thread(target=withdraw_arm_from_bridge).start()
        robot.advance_without_acceleration(59, 500, 0.9)

    if route_3_stage_2:
        time.sleep(0.1)
        robot.retreat(5) # retreat to prepare to turn
        time.sleep(0.1)
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
        time.sleep(0.1)
        robot.advance_without_acceleration(14, 500)
        time.sleep(0.1)
        print(robot.left_wheel.get_vel(), robot.right_wheel.get_vel())
    
        if route_3_go_home:
            robot.retreat_without_acceleration(40)
            robot.turn(15)
            robot.retreat_without_acceleration(80)
        else:
            robot.retreat_time(0.5, 1000)
            robot.stop('hold')

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

def push_train():
    lower_left_motor()
    robot.advance(74)
    raise_left_motor()

def route_1():
    print("route 1")
    robot.advance(84, 300, 0.979)
    time.sleep(0.1)
    robot.turn(33)
    robot.advance(84.5, 400, 0.98)
    time.sleep(0.1)
    robot.turn(89)
    put_down_fork()
    robot.advance(24, 400, 0.979)
    lower_left_motor()
    
    threading.Thread(target=lift_fork).start()
    threading.Thread(target=raise_left_motor).start()
    robot.retreat(41, 300)

    # push train
    lower_left_motor()
    robot.advance(44, 1000, 0.94)    
    time.sleep(0.1)

    # go home
    threading.Thread(target=raise_left_motor).start()
    robot.retreat(19)
    time.sleep(0.1)
    robot.turn(87)
    robot.advance(86, 500, 0.98)
    robot.turn(-29)
    robot.advance(25, 300)
    robot.turn(38)
    robot.advance(65, 1000)

def push_green_and_switch_engine():
    robot.advance(24)

def pull_small_plane():
    robot.right_motor.spin_for_deg(1800)

def pull_big_plane():
    robot.left_motor.spin_for_deg(-700)

def release_grey_cargo():
    robot.left_motor.spin_for_deg(600)

def route_2():
    print("route 2")
    robot.advance(67, 300)
    time.sleep(0.1)
    robot.turn(40)
    time.sleep(0.1)
    push_green_and_switch_engine()
    time.sleep(0.1)
    robot.retreat(17, 300)
    pull_big_plane()
    pull_small_plane()
    robot.retreat(8)
    release_grey_cargo()
    robot.retreat_without_acceleration(50, 1000, 1.3)

def crane_pusher_go_out():
    # robot.right_motor.spin_for_deg(2500)
    robot.right_motor.spin_for_deg(4000)

def pull_back_crane_pusher():
    robot.right_motor.spin_for_deg(-4050)

def accidence_avoidance():
    robot.advance_to_colour(parameters.Color.BLACK, 100)
    robot.advance_without_acceleration(2.9, 75)

def push_small_truck():
    robot.left_motor.spin_for_deg(-300, 500)
    threading.Thread(target=accidence_avoidance).start()
    robot.left_motor.spin_for_deg(-1300)

def route_4():
    print("route 4")
    robot.advance(76, 300, 0.979)
    time.sleep(0.1)
    robot.turn(33)
    robot.advance(38.5, 300, 0.95)
    time.sleep(0.1)
    robot.turn(-85)
    robot.advance(20.5, 300, 0.979)
    time.sleep(0.1)
    crane_pusher_go_out()
    # robot.right_motor.spin_for_deg(-2520)
    threading.Thread(target=lambda: robot.right_motor.spin_for_deg(-4000)).start()
    robot.retreat(10, 150)
    robot.turn(-43)
    robot.advance(41.5, 300, 1.21)
    robot.turn(-10)
    time.sleep(0.2)
    robot.retreat_without_acceleration(3, 500)
    push_small_truck()


robot.brick.speaker.set_volume(20)
debug = False
robot.brick.speaker.beep(440, 200)
if debug:
    # robot.advance(10)
    # time.sleep(0.1)
    # robot.retreat(7, 300)
    # time.sleep(0.1)
    # robot.retreat(8)
    crane_pusher_go_out()
    threading.Thread(target=lambda: robot.right_motor.spin_for_deg(-4000)).start()
    robot.retreat(10, 150)
else:
    # print(f"Battery:", robot.brick.battery.voltage())
    while True:
        if parameters.Button.CENTER in robot.brick.buttons.pressed():
            # wait for release
            while parameters.Button.CENTER in robot.brick.buttons.pressed():
                time.sleep(0.1)
            
            attachment_color = robot.colour_middle.color()
            print(attachment_color)
            robot.brick.speaker.beep(440, 200)
            if attachment_color == parameters.Color.RED:
                route_1()
            elif attachment_color == parameters.Color.BLACK:
                route_2()
            elif attachment_color == parameters.Color.BLUE:
                route_3()
            elif attachment_color == parameters.Color.YELLOW:
                route_4()
            robot.brick.speaker.beep(440, 200)
