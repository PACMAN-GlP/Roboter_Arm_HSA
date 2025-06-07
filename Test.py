import time

from GPTPose import GPTPose

Pose1 = GPTPose(1, 1, 1, 5, True)
Pose2 = GPTPose(1, 1, 2, 5, True)

for i in range(3):
    Pose1.move_servos_to_pose()
    time.sleep(1)
    Pose2.move_servos_to_pose()
    time.sleep(1)

Pose1.reset_Pose_to_auto_home()
Pose1.move_servos_to_pose()
print(Pose1.toString())
time.sleep(1)