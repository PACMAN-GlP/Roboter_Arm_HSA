from __future__ import division
import time
import Adafruit_PCA9685

from Test1 import servo_limits


class Servo:
    pwm = Adafruit_PCA9685.PCA9685(busnum=1)

    """
    servo_limits = {
        0: (100, 510),  # DM996 15kg
        1: (100, 510),  # DM996 15kg
        2: (100, 510),  # DM996 15kg
        3: (100, 510),  # DS3225 25kg
        4: (100, 510),  # 9g Microservo
    }
    """

    pwm.set_pwm_freq(44)

    def __init__(self, servo_id:int, servo_angle:float):
        self.servo_id = servo_id
        self.servo_angle = servo_angle
        self.servo_min = 100 #servo_limits[servo_id][0]
        self.servo_max = 510 #servo_limits[servo_id][1]

    def move(self, angle:float):
        self.servo_angle = angle
        self.pwm.set_pwm(self.servo_id, 0, self.servo_min + (self.servo_max - self.servo_min) * self.servo_angle / 180)

    def get_angle(self):
        return self.servo_angle

    def set_min(self, min:int):
        self.servo_min = min

    def set_max(self, max:int):
        self.servo_max = max

    def get_servo_id(self):
        return self.servo_id

    def get_servo_min(self):
        return self.servo_min

    def get_servo_max(self):
        return self.servo_max

    def __del__(self):
        self.pwm.set_pwm(self.servo_id, 0, 0)