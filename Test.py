import time
from Pose import Pose
from GPTPose import GPTPose

Pose1 = Pose(80, 0, 70, 5, True)
Pose2 = Pose(40, 0, 70, 5, True)

for i in range(3):
    Pose1.move_Servos_To_Pose()
    time.sleep(1)
    Pose2.move_Servos_To_Pose()
    time.sleep(1)
    print(f"Pose 1: {Pose1.toString()} | Pose 2: {Pose2.toString()}")

Pose1.reset_Pose_to_auto_home()
Pose1.move_Servos_To_Pose()
time.sleep(1)
print(Pose1.toString())