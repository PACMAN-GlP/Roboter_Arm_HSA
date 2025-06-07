import math

S1=S2=90
x=y=z=r=0
e=False
S2AngleOffset=20

def get_axis_values():
    if math.sqrt(x ** 2 + y ** 2 + z ** 2) > (S1 + S2):  # Check if distance to target exceeds maximum reach of S1+S2
        raise ValueError(f"Target position is unreachable. make sure the distance does not exceed {S1 + S2}mm.")

    l = math.sqrt(x ** 2 + y ** 2 + z ** 2)  # Distance to target point

    a0 = int(math.degrees(math.atan2(x, y)))
    a1 = int(math.degrees(math.acos(((S1 ** 2 + l ** 2) - S2 ** 2) / (2 * S1 * l))) + math.degrees(math.atan2(z, math.sqrt(x ** 2 + y ** 2))))
    a2 = 180-int(math.degrees(math.acos(((S1 ** 2 + S2 ** 2) - l ** 2) / (2 * S1 * S2))))
    a3 = 90-a1+a2
    if e:
        a4 = 180
    else:
        a4 = 0

    return [a0, a1, a2, a3, a4]

def GPT_axis_values():
    # Distanz zur Zielposition
    l = math.sqrt(x**2 + y**2 + z**2)
    if l > (S1 + S2):
        raise ValueError(f"Ziel {l:.2f}mm ist außerhalb der Reichweite von {S1 + S2}mm.")

    # Winkel A0 - Rotation um Z (Grundrotation)
    a0 = int(math.degrees(math.atan2(x, y)))

    # Berechne A1
    v1 = ((S1**2 + l**2) - S2**2) / (2 * S1 * l)
    v1 = min(1.0, max(-1.0, v1))
    a1_1 = math.degrees(math.acos(v1))
    a1_2 = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))
    a1 = int(a1_1 + a1_2)

    # Berechne A2
    v2 = ((S1**2 + S2**2) - l**2) / (2 * S1 * S2)
    v2 = min(1.0, max(-1.0, v2))
    a2 = 180-int(math.degrees(math.acos(v2)))

    # Berechne A3 (Restwinkel minus bisherige Rotation)
    a3 = int(r - a1 - a2 + S2AngleOffset)
    a4 = int(e)
    return [a0, a1, a2, a3, a4]

x=10
y=0
z=0
r=90
e=False
liste=get_axis_values()
print(f"a0:{liste[0]}, a1:{liste[1]}, a2:{liste[2]}, a3:{liste[3]}, a4:{liste[4]}")
liste=GPT_axis_values()
print(f"GPT → a0:{liste[0]}, a1:{liste[1]}, a2:{liste[2]}, a3:{liste[3]}, a4:{liste[4]}")