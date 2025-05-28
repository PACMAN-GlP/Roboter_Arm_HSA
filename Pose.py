import math
class Pose:
    def __init__(self, x, y, z, r, e):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.e = e

    def get_axis_values(self):
        a0=math.tan(self.z/self.x)
        a1=0
        a2=0
        a3=0
        a4=0
        return [a0, a1, a2, a3, a4]