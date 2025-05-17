import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# I2C-Verbindung aufbauen
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50 Hz für Servos

# Hilfsfunktion: Winkel zu Pulsbreite (zwischen 0 und 0xFFFF)
def set_servo_angle(channel, angle):
    min_pulse = 150  # Minimaler Puls (kann je nach Servo leicht variieren)
    max_pulse = 600  # Maximaler Puls
    pulse = int(min_pulse + (angle / 180.0) * (max_pulse - min_pulse))
    pca.channels[channel].duty_cycle = int((pulse / 4096.0) * 0xFFFF)

# Servo an Kanal 0 schwenken
for angle in range(0, 180, 10):
    set_servo_angle(0, angle)
    time.sleep(0.05)

for angle in range(180, 0, -10):
    set_servo_angle(0, angle)
    time.sleep(0.05)