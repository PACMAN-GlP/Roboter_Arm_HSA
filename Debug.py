import math

x=0
y=0
z=40
S1=S2=90
l=50
a12=math.degrees(math.atan2(z, math.sqrt(x**2+y**2)))
print(a12)
print("ergebnis", int(180-(math.degrees(math.acos((S1 ** 2 + S2 ** 2 - l ** 2) / (2 * S1 * S2)))-25)))