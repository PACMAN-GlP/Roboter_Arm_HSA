from __future__ import division
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685(busnum=1)

servo_limits = {
    0: (100, 510),  # DM996 15kg
    1: (100, 510),  # DM996
<<<<<<< Updated upstream
    2: (205, 410),  # DM996
    3: (150, 600),  # DS3225 25kg
    4: (120, 500),  # 9g Microservo
=======
    2: (100, 510),  # DM996
    3: (100, 510),  # DS3225 25kg
    4: (100, 510),  # 9g Microservo
>>>>>>> Stashed changes
}

# Frequency of the servos
pwm.set_pwm_freq(44)

print('Moving servos (Testbetrieb)...')

while True:
<<<<<<< Updated upstream
    # Move servo on channel O between extremes.
    pwm.set_pwm(0, 0, servo_limits[0][0])
    pwm.set_pwm(1, 0, servo_limits[0][0])
    pwm.set_pwm(2, 0, servo_limits[1][0])
    time.sleep(1)
    pwm.set_pwm(0, 0, servo_limits[0][1])
    pwm.set_pwm(1, 0, servo_limits[0][1])
    pwm.set_pwm(2, 0, servo_limits[1][1])
    time.sleep(1)
=======
    for j in range(2):
        for i in range(5):
            pwm.set_pwm(i, 0, servo_limits[i][j])
        time.sleep(1)
>>>>>>> Stashed changes
