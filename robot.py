import pybricks.hubs as hub
import pybricks.ev3devices as devices
import pybricks.parameters as parameters
import pybricks.robotics as robotics
import motor
import time

class Robot:
    steady_acceleration_constant = 4
    straight_line_adherence_constant = -0.4
    large_motor_max = 1000
    c_to_d = 18.364031
    left_scaling = 0.984

    def __init__(self):

        self.left_motor = motor.Motor(parameters.Port.A)
        self.left_wheel = motor.Motor(parameters.Port.B)
        self.right_wheel = motor.Motor(parameters.Port.C)
        self.right_motor = motor.Motor(parameters.Port.D)
        self.brick = hub.EV3Brick()

        self.colour_left = devices.ColorSensor(parameters.Port.S2)
        self.colour_right = devices.ColorSensor(parameters.Port.S3)
        self.colour_middle = devices.ColorSensor(parameters.Port.S1)
        self.gyro = devices.GyroSensor(parameters.Port.S4)

        # self.drivebase = robotics.DriveBase(self.left_wheel.device, self.right_wheel.device, 62.4, 150)
        # self.drivebase.settings(100, 20, 100, 20)

        self.left_wheel.set_scaling(Robot.left_scaling)
        self.reset_and_calibrate()
        self.stop_mode = "hold"
    
    def reset_and_calibrate(self) -> None:
        self.reset_motors()
        self.calibrate_gyro()
    
    def reset_motors(self) -> None:
        self.reset_wheels()
        self.left_motor.reset()
        self.right_motor.reset()
    
    def reset_wheels(self):
        # start = time.time()
        left_wheel_deg, right_wheel_deg = self.left_wheel.get_deg(), self.right_wheel.get_deg()
        while left_wheel_deg or right_wheel_deg:
            self.left_wheel.reset()
            self.right_wheel.reset()
            left_wheel_deg, right_wheel_deg = self.left_wheel.get_deg(), self.right_wheel.get_deg()
        #     print("RESET: DEG", self.left_wheel.get_deg(), self.right_wheel.get_deg())
        #     print("RESET: VEL", self.left_wheel.get_vel(), self.right_wheel.get_vel())
        # print("RESET TIME:", time.time() - start)
        print("After reset wheels", left_wheel_deg, right_wheel_deg)

    def calibrate_gyro(self, delay: int = 0.1) -> None:
        self.reset_gyro()
        while self.gyro.speed():
            temp = self.gyro.speed()
            temp = self.gyro.angle()
            time.sleep(delay)
    
    def reset_gyro(self) -> None:
        while self.gyro.angle():
            self.gyro.reset_angle(0)
            time.sleep(0.01)
    
    def start_moving_direction(self, direction: (int, float) = 0, vel: (int, float) = 0):
        # print("START MOVING", vel, direction)
        if vel:
            left_vel = vel
            right_vel = vel
        else:
            left_vel = self.left_wheel.get_vel()
            right_vel = self.right_wheel.get_vel()
        if direction > 0:
            right_vel *= 1 - direction / 50
        elif direction < 0:
            left_vel *= 1 + direction / 50
        print("vel:", left_vel, right_vel)
        self.left_wheel.set_vel(left_vel)
        self.right_wheel.set_vel(right_vel)
        self.left_wheel.start()
        self.right_wheel.start()
        print("speed", self.left_wheel.get_speed(), self.right_wheel.get_speed())
    
    def set_stop_mode(self, value: str) -> None:
        self.stop_mode = value
        self.left_wheel.set_stop_mode(value)
        self.right_wheel.set_stop_mode(value)
    
    def stop(self, stop_mode: str = "") -> None:
        if not stop_mode:
            stop_mode = self.stop_mode
        self.left_wheel.stop(stop_mode)
        self.right_wheel.stop(stop_mode)
        self.left_wheel.set_vel(0)
        self.right_wheel.set_vel(0)

    def advance_by_deg(self, deg: (int, float), vel: (int, float) = 1000, left_scaling: float = 0.0) -> None:
        if left_scaling:
            self.left_wheel.set_scaling(left_scaling)
        self.reset_wheels()
        cur_vel = 0
        if vel > 0:
            acceleration = Robot.steady_acceleration_constant
            dif_scaling = Robot.straight_line_adherence_constant
        elif vel < 0:
            acceleration = -Robot.steady_acceleration_constant
            dif_scaling = -Robot.straight_line_adherence_constant

        timeout = 0.5
        previous_left_deg, previous_right_deg = self.left_wheel.get_deg(), self.right_wheel.get_deg()
        previous_time = time.time()
        while abs(self.left_wheel.get_deg()) < deg and abs(self.right_wheel.get_deg()) < deg:
            if abs(cur_vel) < abs(vel):
                cur_vel += acceleration
                self.left_wheel.set_vel(cur_vel)
                self.right_wheel.set_vel(cur_vel)
            left_deg, right_deg = self.left_wheel.get_deg(), self.right_wheel.get_deg()
            dif = right_deg - left_deg
            print(left_deg, right_deg)
            self.start_moving_direction(dif * dif_scaling, cur_vel)

            if left_deg == previous_left_deg and right_deg == previous_right_deg:
                # no more moving
                if time.time() - previous_time > 0.5:
                    break
            else:
                previous_left_deg = left_deg
                previous_right_deg = right_deg
                previous_time = time.time()

        self.stop()
        self.left_wheel.set_scaling(Robot.left_scaling)
    
    def advance(self, cm: (int, float), vel: (int, float) = 500, left_scaling: float = 0.0) -> None:
        print("ADVANCE", cm, "START")
        self.advance_by_deg(cm * Robot.c_to_d, vel, left_scaling)
        print("ADVANCE", cm, "END")
    
    def advance_to_colour(self, colour: parameters.Color = parameters.Color.BLACK, vel: (int, float) = 500, left_scaling: float = 0.0) -> None:
        if left_scaling:
            self.left_wheel.set_scaling(left_scaling)
        self.reset_wheels()
        cur_vel = 0
        if vel > 0:
            acceleration = Robot.steady_acceleration_constant
            dif_scaling = Robot.straight_line_adherence_constant
        elif vel < 0:
            acceleration = -Robot.steady_acceleration_constant
            dif_scaling = -Robot.straight_line_adherence_constant

        while self.colour_right.color() != colour:
            print(self.colour_right.color())
            if abs(cur_vel) < abs(vel):
                cur_vel += acceleration
                self.left_wheel.set_vel(cur_vel)
                self.right_wheel.set_vel(cur_vel)
            left_deg, right_deg = self.left_wheel.get_deg(), self.right_wheel.get_deg()
            dif = right_deg - left_deg
            self.start_moving_direction(dif * dif_scaling, cur_vel)

        self.stop()
        self.left_wheel.set_scaling(Robot.left_scaling)
    
    def advance_with_gyro(self, cm: (int, float), vel: (int, float) = 300) -> None:
        print("advance_with_gyro ", cm)
        self.left_wheel.set_scaling(1)
        self.reset_wheels()
        deg = cm * Robot.c_to_d
        angle = self.gyro.angle()
        cur_vel = 0
        if vel > 0:
            acceleration = Robot.steady_acceleration_constant
        elif vel < 0:
            acceleration = -Robot.steady_acceleration_constant
        while abs(self.left_wheel.get_deg()) < deg and abs(self.right_wheel.get_deg()) < deg:
            if abs(cur_vel) < abs(vel):
                cur_vel += acceleration
                self.left_wheel.set_vel(cur_vel)
                self.right_wheel.set_vel(cur_vel)
            left_deg, right_deg = self.left_wheel.get_deg(), self.right_wheel.get_deg()
            cur_angle = self.gyro.angle()
            deviation = cur_angle - angle
            print(deviation, cur_angle, angle)
            self.start_moving_direction(deviation * -15.0, cur_vel)
        self.stop()
        self.left_wheel.set_scaling(Robot.left_scaling)
    
    def advance_without_acceleration(self, cm: (int, float), vel: (int, float) = 500, left_scaling: float = 0.0) -> None:
        print("ADVANCE WITHOUT ACCELERATION", cm, "START")
        deg = cm * Robot.c_to_d
        if left_scaling:
            self.left_wheel.set_scaling(left_scaling)
        self.reset_wheels()
        self.left_wheel.set_vel(vel)
        self.right_wheel.set_vel(vel)
        if vel > 0:
            dif_scaling = Robot.straight_line_adherence_constant
        elif vel < 0:
            dif_scaling = -Robot.straight_line_adherence_constant
        while abs(self.left_wheel.get_deg()) < deg and abs(self.right_wheel.get_deg()) < deg:
            left_deg, right_deg = self.left_wheel.get_deg(), self.right_wheel.get_deg()
            dif = right_deg - left_deg
            self.start_moving_direction(dif * dif_scaling, vel)
        self.left_wheel.set_scaling(Robot.left_scaling)
        self.stop()
        print("ADVANCE WITHOUT ACCELERATION", cm, "END")    
    
    def advance_drivebase(self, cm):
        self.drivebase.straight(cm * 10)
    
    def advance_time(self, sec: (int, float), vel: (int, float) = 500, left_scaling: float = 0.0):
        print("ADVANCE TIME", sec, "START")
        if left_scaling:
            self.left_wheel.set_scaling(left_scaling)
        self.reset_wheels()
        target = time.time() + sec
        self.start_moving_direction(0, vel)
        while time.time() < target:
            time.sleep(0.01)
        self.stop()
        self.left_wheel.set_scaling(Robot.left_scaling)
        print("ADVANCE TIME", sec, "END")

    def retreat(self, cm: (int, float), vel: (int, float) = 500, left_scaling: float = 0.0) -> None:
        print("RETREAT", cm, "START")
        self.advance(cm, -vel, left_scaling)
        print("RETREAT", cm, "END")

    def retreat_without_acceleration(self, cm: (int, float), vel: (int, float) = 500, left_scaling: float = 0.0) -> None:
        self.advance_without_acceleration(cm, -vel, left_scaling)
    
    def retreat_time(self, sec: (int, float), vel: (int, float) = 500, left_scaling: float = 0.0):
        print("RETREAT TIME", sec, "START")
        self.advance_time(sec, -vel, left_scaling)
        print("RETREAT TIME", sec, "END")

    def turn(self, deg: (int, float), vel: (int, float) = 150) -> None:
        print("TURN", deg, "START")
        if deg > 0:
            direction = 100
        elif deg < 0:
            direction = -100
        self.reset_wheels()
        self.reset_gyro()
        self.start_moving_direction(direction, vel)
        deg = abs(deg)
        last_angle = 0
        while True:
            angle = abs(self.gyro.angle())
            if abs(angle - last_angle) > 10:
                print(angle)
                print("wrong angle")
                self.gyro.reset_angle(last_angle + 1)
                print(last_angle)
                continue
            print(angle, deg)
            last_angle = angle
            if angle >= deg:
                break
            time.sleep(0.01)
        self.stop()
        print("TURN", deg, "END")
    
    def pivot(self, deg: (int, float), vel: (int, float) = 150) -> None:
        print("PIVOT", deg, "START")
        if deg > 0:
            direction = 50
        elif deg < 0:
            direction = -50
        self.reset_wheels()
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
        print("PIVOT", deg, "END")
