import math
class Pose:
    S1=90 #Length of arm a1 to a2
    S2=90 #Length of arm a2 to a3
    S2AngleOffset=20 #Angle offset to a3 due to geometry of a2

    def __init__(self, x, y, z, r, e):
        self.reset_Pose_to_auto_home()
        self.change_Pose(x, y, z, r, e)
        self.get_axis_values()

    def get_axis_values(self):
        if math.sqrt(self.x**2+self.y**2+self.z**2) > (Pose.S1+Pose.S2): #Check if distance to target exceeds maximum reach of S1+S2
            raise ValueError(f"Target position is unreachable. make sure the distance does not exceed {Pose.S1+Pose.S2}mm.")

        l=math.sqrt(self.x**2+self.y**2+self.z**2)
        if l==0:
            l=0.00001
        a12=math.degrees(math.atan2(self.z, math.sqrt(self.x**2+self.y**2)))

        if self.x==0 and self.y==0:
            self.a0=90
        else:
            self.a0=int(math.degrees(math.atan2(self.x, self.y)))
        self.a1 = int(180-(math.degrees(math.acos(((self.S1**2 + l**2 - self.S2**2) / (2 * self.S1 * l)))) + a12))
        self.a2 = int(180 -(math.degrees(math.acos((self.S1 ** 2 + self.S2 ** 2 - l ** 2) / (2 * self.S1 * self.S2)))-25))

        return [self.a0, self.a1, self.a2, self.a3, self.a4]

    def change_Pose(self, x, y, z, r, e:bool):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.e = e
        self.get_axis_values()

    def reset_Pose_to_auto_home(self):
        self.a0=90
        self.a1=0
        self.a2=180
        self.a3=90
        self.a4=0

    def axisToString(self):
        return f"{self.a0}, {self.a1}, {self.a2}, {self.a3}, {self.a4}"

    def posToString(self):
        return f"{self.x}, {self.y}, {self.z}"