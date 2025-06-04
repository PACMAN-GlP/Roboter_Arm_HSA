import sys

# Winkel aus Kommandozeile holen
angles = list(map(int, sys.argv[1:]))

# Hier würdest du deine Servo- oder Motorsteuerung integrieren
print("Empfangene Winkel:", angles)

# Beispiel: GPIO-Steuerung (nur angedeutet)
# import RPi.GPIO as GPIO
# servo1.set_angle(angles[0])
# servo2.set_angle(angles[1])
# ...
