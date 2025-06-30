import time
from Pose import Pose
from Servo import Servo
import numpy as np

class Kinematics:
    def __init__(self):
        self.Pose0 = Pose(0, 0, 0, 0, 0)
        self.Pose0.reset_Pose_to_auto_home()
        self.move_p2p(self.Pose0)

    def move_lin(self, target: Pose, steps: int = 50, wait_per_step: float = 0.01):
        # Aktuelle Position aus self.Pose0 übernehmen
        start = self.Pose0
        dx = (target.x - start.x) / steps
        dy = (target.y - start.y) / steps
        dz = (target.z - start.z) / steps
        dr = (target.r - start.r) / steps
        de = (target.e - start.e) / steps  # Sollte e bool sein, wird es zu float 0.0 oder 1.0

        for i in range(1, steps + 1):
            # Zwischenschritt berechnen
            intermediate_pose = Pose(
                start.x + dx * i,
                start.y + dy * i,
                start.z + dz * i,
                start.r + dr * i,
                bool(round(start.e + de * i))  # wandelt zurück zu bool
            )
            self.move_p2p(intermediate_pose, wait=wait_per_step)

        self.Pose0 = target  # Zielpose merken

    def move_p2p(self, pos:Pose, wait:float=1):
        print(f"{pos.a0}, {pos.a1}, {pos.a2}, {pos.a3}, {pos.a4}")
        servo0 = Servo(0)
        servo1 = Servo(1)
        servo2 = Servo(2)
        servo3 = Servo(3)
        servo4 = Servo(4)
        servo0.set_angle(pos.a0)
        servo1.set_angle(pos.a1)
        servo2.set_angle(pos.a2)
        servo3.set_angle(pos.a3)
        servo4.set_angle(pos.a4)
        time.sleep(wait)