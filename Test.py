from Kinematics import Kinematics
from Pose import Pose

Pose1 = Pose(80, 0, 70, 5, True)
Pose2 = Pose(40, 0, 70, 5, True)
Kin = Kinematics()


for i in range(3):
    Kin.lin_move_p2p(Pose1, 30)

    Kin.lin_move_p2p(Pose2, 30)

Pose1.reset_Pose_to_auto_home()
Kin.joint_move_p2p(Pose1)
print(Pose1.axisToString())