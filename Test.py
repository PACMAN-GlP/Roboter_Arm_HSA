from Kinematics import Kinematics
from Pose import Pose

Pose1 = Pose(40, 20, 70, 5, True)
Pose2 = Pose(40, -20, 70, 5, True)
Kin = Kinematics()

for i in range(3):
    Kin.move_lin(Pose1)

    Kin.move_lin(Pose2)

Pose1.reset_Pose_to_auto_home()
Kin.move_p2p(Pose1)
print(Pose1)