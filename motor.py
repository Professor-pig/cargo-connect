import pybricks.ev3devices as devices
import pybricks.parameters as parameters


class Motor:
    stopping = {
        "coast": parameters.Stop.COAST,
        "brake": parameters.Stop.BRAKE,
        "hold": parameters.Stop.HOLD
    }

    def __init__(self, port):
        self.device = devices.Motor(port, parameters.Direction.COUNTERCLOCKWISE)
        self.scaling = 1.0
        self.stop_mode = "brake"
        self.stop_function = {
            "coast": self.device.stop,
            "brake": self.device.brake,
            "hold": self.device.hold
        }
        self.vel = float()
    
    def set_scaling(self, value: float) -> None:
        self.scaling = value
    
    def set_stop_mode(self, value: str) -> None:
        self.stop_mode = value
    
    def set_vel(self, value: (int, float)) -> None:
        self.vel = float(value)
    
    def get_vel(self) -> float:
        return self.vel
    
    def get_deg(self) -> (int, float):
        angle = self.device.angle() * self.scaling
        return 0 - angle
    
    def reset(self) -> None:
        self.device.reset_angle(0)
    
    def stop(self, stop_mode: str = "") -> None:
        if not stop_mode:
            stop_mode = self.stop_mode
        self.stop_function[stop_mode]()
    
    def start(self) -> None:
        self.device.run(self.vel * self.scaling)
    
    def spin_for_time(self, milliseconds: (int, float), vel: (int, float) = 2000, stop_mode: str = "", wait: bool = True) -> None:
        if not stop_mode:
            stop_mode = self.stop_mode
        if vel:
            vel *= self.scaling
        else:
            vel = self.vel
        self.device.run_time(vel, milliseconds, Motor.stopping[stop_mode], wait)
    
    def spin_for_deg(self, deg: int, vel: (int, float) = 2000, stop_mode: str = "", wait: bool = True) -> None:
        print("spin_for_deg", deg)
        if not stop_mode:
            stop_mode = self.stop_mode
        if not vel:
            vel = self.vel
        self.device.run_angle(vel, -deg * self.scaling, Motor.stopping[stop_mode], wait)
    
    def spin_to(self, pos: int = 0, vel: (int, float) = 2000, stop_mode: str = "") -> None:
        cur_deg = self.device.angle()
        if pos > cur_deg:
            self.device.run(vel)
            while pos > self.device.angle():
                time.sleep(0.01)
            self.device.stop(stop_mode)
        elif pos < cur_deg:
            self.device.run(-vel)
            while pos < self.device.angle():
                time.sleep(0.01)
            self.device.stop(stop_mode)


    def hold(self):
         self.device.hold()   