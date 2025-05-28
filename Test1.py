import time
from Servo import Servo

servo0 = Servo(0)
servo1 = Servo(1)
servo2 = Servo(2)
servo3 = Servo(3)
servo4 = Servo(4)

def auto_home():
    servo0.set_angle(90)
    servo1.set_angle(0)
    servo2.set_angle(180)
    servo3.set_angle(90)
    servo4.set_angle(0)
    time.sleep(1)

def pos1():
    servo0.set_angle(120)
    servo1.set_angle(90)
    servo2.set_angle(45)
    servo3.set_angle(180-45)
    servo4.set_angle(0)
    time.sleep(0.5)

def pos2():
    servo0.set_angle(50)
    servo1.set_angle(90)
    servo2.set_angle(45)
    servo3.set_angle(180 - 45)
    servo4.set_angle(0)
    time.sleep(0.5)

def pos3():
    servo0.set_angle(90)
    servo1.set_angle(90)
    servo2.set_angle(45)
    servo3.set_angle(180 - 45)
    servo4.set_angle(0)
    time.sleep(0.5)

def pos4():
    servo0.set_angle(90)
    servo1.set_angle(90)
    servo2.set_angle(90)
    servo3.set_angle(180 - 45)
    servo4.set_angle(0)
    time.sleep(0.5)

while True:
    auto_home()
    time.sleep(1)
    for i in range(3):
        pos1()
        pos2()
    pos3()
    for i in range(3):
        pos4()
        pos3()
    time.sleep(2)