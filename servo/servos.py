'''
Docstring for servo.servos
sets up the pwm output to both servos
angle limits
'''
# servo/pan_tilt.py
import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None


def clamp(v, vmin, vmax):
    return max(vmin, min(vmax, v))


class PanTilt:
    def __init__(
        self,
        pan_pin,
        tilt_pin,
        freq,
        pan_center,
        tilt_center,
        pan_min,
        pan_max,
        tilt_min,
        tilt_max,
        step,
    ):
        if GPIO is None:
            raise RuntimeError("RPi.GPIO not available (must run on Raspberry Pi).")

        self.pan_pin = pan_pin
        self.tilt_pin = tilt_pin
        self.freq = freq

        self.pan_center = pan_center
        self.tilt_center = tilt_center

        self.pan_min = pan_min
        self.pan_max = pan_max
        self.tilt_min = tilt_min
        self.tilt_max = tilt_max

        self.step = step

        self.pan_dc = pan_center
        self.tilt_dc = tilt_center

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pan_pin, GPIO.OUT)
        self.pan_pwm = GPIO.PWM(self.pan_pin, self.freq)
        self.pan_pwm.start(0)

        self.tilt_pwm = None
        if self.tilt_pin is not None:
            GPIO.setup(self.tilt_pin, GPIO.OUT)
            self.tilt_pwm = GPIO.PWM(self.tilt_pin, self.freq)
            self.tilt_pwm.start(0)

        # Center
        self.set_pan(self.pan_center)
        if self.tilt_pwm:
            self.set_tilt(self.tilt_center)

        time.sleep(0.2)

    def set_pan(self, duty):
        self.pan_dc = clamp(duty, self.pan_min, self.pan_max)
        self.pan_pwm.ChangeDutyCycle(self.pan_dc)

    def set_tilt(self, duty):
        if not self.tilt_pwm:
            return
        self.tilt_dc = clamp(duty, self.tilt_min, self.tilt_max)
        self.tilt_pwm.ChangeDutyCycle(self.tilt_dc)

    def update_from_error(self, error_x, error_y=0):
        # Flip signs here if servo moves opposite direction
        if error_x > 0:
            self.set_pan(self.pan_dc - self.step)
        elif error_x < 0:
            self.set_pan(self.pan_dc + self.step)

        if self.tilt_pwm:
            if error_y > 0:
                self.set_tilt(self.tilt_dc - self.step)
            elif error_y < 0:
                self.set_tilt(self.tilt_dc + self.step)

    def close(self):
        self.pan_pwm.stop()
        if self.tilt_pwm:
            self.tilt_pwm.stop()
        GPIO.cleanup()
