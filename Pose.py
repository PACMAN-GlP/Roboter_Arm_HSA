import math
class Pose:
    S1=5 #Length of arm a1 to a2
    S2=5 #Length of arm a2 to a3
    def __init__(self, x, y, z, r, e):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.e = e

    def get_axis_values(self, l1:float, l2:float, l3:float):
        l=math.sqrt(l1**2+l2**2+l3**2) #Distance to target point
        if math.sqrt(l1**2+l2**2+l3**2) > (Pose.S1+Pose.S2): #check if distance to target exceeds maximum reach of S1+S2
            return None
        a0=int(math.degrees(math.atan(self.x/self.y)))
        a1=int(math.degrees(math.acos(((Pose.S1**2+l**2)-Pose.S2**2)/(2*Pose.S1*l)))+math.degrees(math.atan(l3/math.sqrt(l1**2+l2**2))))
        a2=int(math.degrees(math.acos(((Pose.S1**2+Pose.S2**2)-l**2)/(2*Pose.S1*Pose.S2))))
        a3=0
        a4=0
        return [a0, a1, a2, a3, a4]