'''
sets up the pwm output to both servos
angle limits
'''

import RPi.GPIO as GPIO

class Servo:
    def __init__(self, pin, freq, min_dc, max_dc, center_dc):
        self.pin = pin
        self.freq = freq
        self.min_dc = min_dc
        self.max_dc = max_dc
        self.dc = center_dc

        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, freq)
        self.pwm.start(0)

    def set_duty(self, duty):
        self.dc = max(self.min_dc, min(self.max_dc, duty))
        self.pwm.ChangeDutyCycle(self.dc)

    def stop(self):
        self.pwm.stop()