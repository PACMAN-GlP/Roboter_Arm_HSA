# Überarbeitete Version von Pose.py
from math import sqrt, atan2, acos, degrees
from Servo import Servo

class GPTPose:
    S1 = 90  # Länge von Arm A1 zu A2 (in mm)
    S2 = 90  # Länge von Arm A2 zu A3 (in mm)
    S2AngleOffset = 20  # Zusätzlicher Offset für A3 (z. B. bei mechanischer Vorspannung)

    def __init__(self, x, y, z, r, e):
        self.change_Pose(x, y, z, r, e)
        self.servo0 = Servo(0)
        self.servo1 = Servo(1)
        self.servo2 = Servo(2)
        self.servo3 = Servo(3)
        self.servo4 = Servo(4)
        self.get_axis_values()

    def get_axis_values(self):
        # Distanz zur Zielposition
        l = sqrt(self.x**2 + self.y**2 + self.z**2)
        if l > (GPTPose.S1 + GPTPose.S2):
            raise ValueError(f"Ziel {l:.2f}mm ist außerhalb der Reichweite von {GPTPose.S1 + GPTPose.S2}mm.")

        # Winkel A0 - Rotation um Z (Grundrotation)
        self.a0 = int(degrees(atan2(self.x, self.y)))

        # Berechne A1
        v1 = ((GPTPose.S1**2 + l**2) - GPTPose.S2**2) / (2 * GPTPose.S1 * l)
        v1 = min(1.0, max(-1.0, v1))
        a1_1 = degrees(acos(v1))
        a1_2 = degrees(atan2(self.z, sqrt(self.x**2 + self.y**2)))
        self.a1 = int(a1_1 + a1_2)

        # Berechne A2
        v2 = ((GPTPose.S1**2 + GPTPose.S2**2) - l**2) / (2 * GPTPose.S1 * GPTPose.S2)
        v2 = min(1.0, max(-1.0, v2))
        self.a2 = int(degrees(acos(v2)))

        # Berechne A3 (Restwinkel minus bisherige Rotation)
        self.a3 = int(self.r - self.a1 - self.a2 + GPTPose.S2AngleOffset)
        self.a4 = int(self.e)

        return [self.a0, self.a1, self.a2, self.a3, self.a4]

    def change_Pose(self, x, y, z, r, e):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.e = e

    def move_servos_to_pose(self):
        angles = self.get_axis_values()
        self.servo0.set_angle(angles[0])
        self.servo1.set_angle(angles[1])
        self.servo2.set_angle(angles[2])
        self.servo3.set_angle(angles[3])
        self.servo4.set_angle(angles[4])

    def reset_Pose_to_auto_home(self):
        self.a0 = 90
        self.a1 = 0
        self.a2 = 180
        self.a3 = 90
        self.a4 = 0

    def toString(self):
        return f"a0: {self.a0}, a1: {self.a1}, a2: {self.a2}, a3: {self.a3}, a4: {self.a4} | x, y, z, r, e: {self.x}, {self.y}, {self.z}, {self.r}, {self.e}"