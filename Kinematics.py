import time
from Pose import Pose
from Servo import Servo
import numpy as np

class Kinematics:
    def __init__(self):
        self.Pose0 = Pose(0, 0, 0, 0, 0)
        self.Pose0.reset_Pose_to_auto_home()
        self.move_p2p(self.Pose0)

    def move_lin(self, target:Pose):
        """
        while self.Pose0.a0 != pos.a0 or self.Pose0.a1 != pos.a1 or self.Pose0.a2 != pos.a2 or self.Pose0.a3 != pos.a3 or self.Pose0.a4 != pos.a4:
            time1 = time.time()
            x=self.Pose0.x+(pos.x-self.Pose0.x)*(time.time()-time1)*speed
            y = self.Pose0.y + (pos.y - self.Pose0.y) * (time.time() - time1)*speed
            z = self.Pose0.z + (pos.z - self.Pose0.z) * (time.time() - time1)*speed
            self.Pose0.change_Pose(int(x), int(y), int(z), pos.r, pos.e)
            self.joint_move_p2p(self.Pose0)
            print(self.Pose0.posToString())
        print("finished!")
        """
        speed=30
        # Extrahiere Start- und Zielvektoren
        p0 = np.array([self.Pose0.x, self.Pose0.y, self.Pose0.z, self.Pose0.r, self.Pose0.e])
        p1 = np.array([target.x, target.y, target.z, target.r, target.e])

        dist = np.linalg.norm(p1 - p0)  # Gesamtdistanz
        duration = dist / speed if speed > 0 else 1  # Sekunden
        steps = int(duration / 0.05)  # ca. 20 Hz, alle 50 ms
        if steps < 1:
            steps = 1

        for i in range(steps + 1):
            alpha = i / steps  # Fortschritt von 0 bis 1
            interp = (1 - alpha) * p0 + alpha * p1
            pose = Pose(*interp)
            pose.get_axis_values()
            self.Pose0 = pose
            self.move_p2p(pose)
            print(pose.posToString())
            time.sleep(0.05)

        print("finished!")

    def move_p2p(self, pos:Pose):
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
        time.sleep(0.05)