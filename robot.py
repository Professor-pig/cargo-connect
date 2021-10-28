# from pybricks.hubs import EV3Brick
import pybricks.hubs as hub
# from pybricks.ev3devices import Motor, ColorSensor, InfraredSensor, GyroSensor
import pybricks.ev3devices as devices
# from pybricks.parameters import Port, Stop, Direction, Button, Color
import pybricks.parameters as parameters
# from pybricks.robotics import DriveBase
import pybricks.robotics as robotics
import motor
import time

class Robot:
    steady_acceleration_constant = 4
    straight_line_adherence_constant = -0.4
    large_motor_max = 1000
    c_to_d = 18.364031
    B_scaling = 0.984

    def __init__(self):

        self.A = motor.Motor(parameters.Port.A)
        self.B = motor.Motor(parameters.Port.B)
        self.C = motor.Motor(parameters.Port.C)
        self.D = motor.Motor(parameters.Port.D)
        self.brick = hub.EV3Brick()

        self.colour_left = devices.ColorSensor(parameters.Port.S2)
        self.colour_right = devices.ColorSensor(parameters.Port.S3)
        #self.colour_middle = devices.ColorSensor(parameters.Port.S1)
        self.gyro = devices.GyroSensor(parameters.Port.S4)

        # self.drivebase = robotics.DriveBase(self.B.device, self.C.device, 62.4, 150)
        # self.drivebase.settings(100, 20, 100, 20)

        self.B.set_scaling(Robot.B_scaling)
        self.reset_and_calibrate()
        self.stop_mode = "brake"
    
    def reset_and_calibrate(self) -> None:
        self.reset_motors()
        self.calibrate_gyro()
    
    def reset_motors(self) -> None:
        self.A.reset()
        self.B.reset()
        self.C.reset()
        self.D.reset()

    def calibrate_gyro(self, delay: int = 0.1) -> None:
        self.reset_gyro()
        while self.gyro.speed():
            temp = self.gyro.speed()
            temp = self.gyro.angle()
            time.sleep(delay)
    
    def reset_gyro(self) -> None:
        while self.gyro.angle():
            self.gyro.reset_angle(0)
    
    def start_moving_direction(self, direction: (int, float) = 0, vel: (int, float) = 0):
        print("START MOVING", vel, direction)
        if vel:
            B_vel = vel
            C_vel = vel
        else:
            B_vel = self.B.get_vel()
            C_vel = self.C.get_vel()
        if direction > 0:
            C_vel *= 1 - direction / 50
        elif direction < 0:
            B_vel *= 1 + direction / 50
        print(B_vel, C_vel)
        self.B.set_vel(B_vel)
        self.C.set_vel(C_vel)
        self.B.start()
        self.C.start()
    
    def set_stop_mode(self, value: str) -> None:
        self.stop_mode = value
        self.B.set_stop_mode(value)
        self.C.set_stop_mode(value)
    
    def stop(self, stop_mode: str = "") -> None:
        if not stop_mode:
            stop_mode = self.stop_mode
        self.B.stop(stop_mode)
        self.C.stop(stop_mode)

    def advance_by_deg(self, deg: (int, float), vel: (int, float) = 1000, B_scaling: float = 0.0) -> None:
        if B_scaling:
            self.B.set_scaling(B_scaling)
        self.B.reset()
        self.C.reset()
        cur_vel = 0
        if vel > 0:
            acceleration = Robot.steady_acceleration_constant
        elif vel < 0:
            acceleration = -Robot.steady_acceleration_constant
        while abs(self.B.get_deg()) < deg and abs(self.C.get_deg()) < deg:
            if abs(cur_vel) < abs(vel):
                cur_vel += acceleration
                self.B.set_vel(cur_vel)
                self.C.set_vel(cur_vel)
            B_deg, C_deg = self.B.get_deg(), self.C.get_deg()
            dif = C_deg - B_deg
            # print(C_vel)
            self.start_moving_direction(dif * Robot.straight_line_adherence_constant, cur_vel)
        self.B.set_scaling(Robot.B_scaling)
        self.stop()
    
    def advance(self, cm: (int, float), vel: (int, float) = 500, B_scaling: float = 0.0) -> None:
        print("ADVANCE", cm)
        self.advance_by_deg(cm * Robot.c_to_d, vel, B_scaling)
    
    def advance_without_acceleration(self, cm: (int, float), vel: (int, float) = 500, B_scaling: float = 0.0) -> None:
        deg = cm * Robot.c_to_d
        if B_scaling:
            self.B.set_scaling(B_scaling)
        self.B.reset()
        self.C.reset()
        self.B.set_vel(vel)
        self.C.set_vel(vel)
        while abs(self.B.get_deg()) < deg and abs(self.C.get_deg()) < deg:
            B_deg, C_deg = self.B.get_deg(), self.C.get_deg()
            dif = C_deg - B_deg
            self.start_moving_direction(dif * Robot.straight_line_adherence_constant, vel)
        self.B.set_scaling(Robot.B_scaling)
        self.stop()
    
    def advance_drivebase(self, cm):
        self.drivebase.straight(cm * 10)
    
    def retreat(self, cm: (int, float), vel: (int, float) = 500) -> None:
        self.advance(cm, -vel)
    
    def turn(self, deg: (int, float), vel: (int, float) = 150) -> None:
        print("TURN", deg)
        if deg > 0:
            direction = 100
        elif deg < 0:
            direction = -100
        self.reset_motors()
        self.reset_gyro()
        self.start_moving_direction(direction, vel)
        deg = abs(deg)
        while True:
            angle = abs(self.gyro.angle())
            print(angle, deg)
            if angle >= deg:
                break
            time.sleep(0.01)
        self.stop()
    
    def pivot(self, deg: (int, float), vel: (int, float) = 150) -> None:
        print("PIVOT", deg)
        if deg > 0:
            direction = 50
        elif deg < 0:
            direction = -50
        self.reset_motors()
        self.reset_gyro()
        self.start_moving_direction(direction, vel)
        deg = abs(deg)
        while True:
            angle = abs(self.gyro.angle())
            print(angle, deg)
            if angle >= deg:
                break
            time.sleep(0.01)
        self.stop()
            