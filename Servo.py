from __future__ import division #improved compatibility between python 2 and 3
import Adafruit_PCA9685 #servo driver board "firmware". main functions: set_pwm_freq and set_pwm

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

    pwm.set_pwm_freq(44) #corrected measured frequency value; ~50 Hz → T=20 ms

    def __init__(self, servo_id:int, servo_angle:int):
        self.servo_id = servo_id
        self.servo_angle = servo_angle #initial angle
        self.servo_min = 100 #servo_limits[servo_id][0] #corrected measured pulse value; 0,5 ms
        self.servo_max = 500 #servo_limits[servo_id][1] #corrected measured pulse value; 2,5 ms

    def move(self, angle:float): #main move function for servo. use to move servo to specific angle
        angle = int(self.servo_min + (self.servo_max - self.servo_min) * angle / 180)
        if self.servo_max+1 > angle > self.servo_min-1:
            self.servo_angle = angle
        self.pwm.set_pwm(self.servo_id, 0, self.servo_angle)

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