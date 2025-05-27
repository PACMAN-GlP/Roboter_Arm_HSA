import time
from Servo import Servo

servo0 = Servo(0, 90)

while True:
    servo0.move(0)
    time.sleep(1)
    servo0.move(90)
    time.sleep(1)
    servo0.move(180)
    time.sleep(1)