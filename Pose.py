import math
class Pose:
    S1=5 #Length of arm a1 to a2
    S2=5 #Length of arm a2 to a3
    S2AngleOffset=20 #Angle offset to a3 due to geometry of a2

    def __init__(self, x, y, z, r, e):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.e = e

        axis=self.get_axis_values()
        self.a0=axis[0]
        self.a1=axis[1]
        self.a2=axis[2]
        self.a3=axis[3]
        self.a4=axis[4]

    def get_axis_values(self):
        if math.sqrt(self.x**2+self.y**2+self.z**2) > (Pose.S1+Pose.S2): #Check if distance to target exceeds maximum reach of S1+S2
            raise ValueError(f"Target position is unreachable. make sure the distance does not exceed {Pose.S1+Pose.S2}mm.")

        l=math.sqrt(self.x**2+self.y**2+self.z**2) #Distance to target point

        a0=int(math.degrees(math.atan2(self.x,self.y)))
        a1=int(math.degrees(math.acos(((Pose.S1**2+l**2)-Pose.S2**2)/(2*Pose.S1*l)))+math.degrees(math.atan2(self.z,math.sqrt(self.x**2+self.y**2))))
        a2=int(math.degrees(math.acos(((Pose.S1**2+Pose.S2**2)-l**2)/(2*Pose.S1*Pose.S2))))
        """ Falls code von a1/a2 nicht funktioniert...
        v1 = ((Pose.S1**2 + l**2) - Pose.S2**2) / (2 * Pose.S1 * l)
        v1 = min(1, max(-1, v1))
        a1 = int(math.degrees(math.acos(v1)) + math.degrees(...))
        
        v2 = ((Pose.S1**2 + Pose.S2**2) - l**2) / (2 * Pose.S1 * Pose.S2)
        v2 = min(1, max(-1, v2))
        a2 = int(math.degrees(math.acos(v2)))
        """
        a3=self.r-a1-a2+Pose.S2AngleOffset
        a4=self.e

        return [a0, a1, a2, a3, a4]

    def reset_Pose_to_auto_home(self):
        self.a0=90
        self.a1=0
        self.a2 =180
        self.a3 =90
        self.a4 =0
