import sys
from Pose import Pose
from Servo import Servo

servo0 = Servo(0)
servo1 = Servo(1)
servo2 = Servo(2)
servo3 = Servo(3)
servo4 = Servo(4)

def set_servos(a0, a1, a2, a3, a4):
    servo0.set_angle(a0)
    servo1.set_angle(a1)
    servo2.set_angle(a2)
    servo3.set_angle(a3)
    servo4.set_angle(a4)

angles = list(map(int, sys.argv[1:]))
print(f"Empfangene Winkel: {angles}")

set_servos(angles[0], angles[1], angles[2], angles[3], angles[4])