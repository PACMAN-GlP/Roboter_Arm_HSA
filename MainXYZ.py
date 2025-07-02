from Kinematics import Kinematics
from Pose import Pose
import sys

Pose1 = Pose(0, 0, 0, 90, False)
Kinematics1 = Kinematics()

def set_servos(x, y, z, r):
    Pose1.change_Pose(x, y, z, r, Pose1.e)
    Kinematics1.move_p2p(Pose1)
    
values = list(map(float, sys.argv[1:]))
print(f"Empfangene Werte: {values}")

set_servos(values[0], values[1], values[2], values[3])