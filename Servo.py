from __future__ import division #improved compatibility between python 2 and 3
import Adafruit_PCA9685 #servo driver board "firmware". main functions: set_pwm_freq and set_pwm

class Servo:
    pwm = Adafruit_PCA9685.PCA9685(busnum=1)

    servo_limits = {
        0: (100, 510),  # DM996 15kg
        1: (85, 450),  # DS3225 25kg
        2: (145, 510),  # DM996 15kg 0°-165°
        3: (100, 510),  # DM996 15kg
        4: (200, 300),  # 9g Microservo
    }

    pwm.set_pwm_freq(44) #corrected measured frequency value; ~50 Hz → T=20 ms

    def __init__(self, servo_id:int):
        self.servo_id = servo_id
        self.servo_min = Servo.servo_limits[servo_id][0] #corrected measured pulse value; 0,5 ms
        self.servo_max = Servo.servo_limits[servo_id][1] #corrected measured pulse value; 2,5 ms
        self.servo_pulse = self.angle_to_pulse(90)
        self.pwm.set_pwm(self.servo_id, 0, self.servo_pulse)

    def set_angle(self, angle):
        pulse = self.angle_to_pulse(angle)
        if self.servo_min <= pulse <= self.servo_max:
            self.pwm.set_pwm(self.servo_id, 0, pulse)
            self.servo_pulse = pulse
        print(angle)

    def angle_to_pulse(self, angle):
        return int(self.servo_min + (self.servo_max - self.servo_min) * angle / 180)

    def pulse_to_angle(self, pulse):
        return int(180 * (pulse - self.servo_min) / (self.servo_max - self.servo_min))

    def get_angle(self):
        return self.pulse_to_angle(self.servo_pulse)

    def get_pulse(self):
        return self.servo_pulse